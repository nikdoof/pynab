import os
from json import load
import locale
from pynab.exceptions import InvalidBudget


class EntityList(list):

    def filter(self, key, value):
        return EntityList([x for x in self if x.getattr(key, None) == value])

    def get(self, key, value):
        for x in self:
            if x.getattr(key, None) == value:
                return x


class Entity(dict):

    def __init__(self, budget, *args, **kwargs):
        self._budget = budget
        dict.__init__(self, *args, **kwargs)

    def __repr__(self):
        return u'<{}>'.format(self.__unicode__())

    def __unicode__(self):
        return u'{} ({})'.format(self.id, self.type)

    @property
    def id(self):
        return self['entityId']

    @property
    def type(self):
        return self['entityType']

    @property
    def version(self):
        return self['entityVersion']

    @property
    def name(self):
        return self['name']


class Category(Entity):
    """
    YNAB Budget Category
    """
    pass


class Account(Entity):
    """
    YNAB Account
    """

    @property
    def account_type(self):
        return self['accountType']

    @property
    def note(self):
        return self['note']

    @property
    def hidden(self):
        return self['hidden']

    @property
    def on_budget(self):
        return self['onBudget']

    def __unicode__(self):
        return u'{} ({})'.format(self['accountName'], self['accountType'])


class Budget(object):
    """
    YNAB Budget
    """

    def __init__(self, filename=None):
        self._data = None
        if filename:
            self.load(filename)

    def load(self, filename):

        # Load the budget's metadata
        if not os.path.exists(os.path.join(filename, 'Budget.ymeta')):
            raise InvalidBudget('{} is a invalid YNAB budget')
        with open(os.path.join(filename, 'Budget.ymeta'), 'r') as f:
            meta = load(f)

        # Find the relative folder name
        data_folder = os.path.join(filename, meta['relativeDataFolderName'])

        # Check the devices, and see which is tagged with full knowledge
        devices_folder = os.path.join(data_folder, 'devices')
        for device in os.listdir(devices_folder):
            with open(os.path.join(devices_folder, device)) as f:
                device_info = load(f)
                if device_info['hasFullKnowledge']:
                    target_folder = device_info['deviceGUID']
                    break
        else:
            raise InvalidBudget('No device has full budget data')

        # Load the full budget file
        with open(os.path.join(data_folder, target_folder, 'Budget.yfull')) as f:
            self._data = load(f)

    def get_account(self, id):
        """
        Returns an Account entity by ID
        """
        if isinstance(id, list) or isinstance(id, tuple):
            return [x for x in self.accounts if x.id in id]
        else:
            return self.accounts.get(id)

    @property
    def budget_type(self):
        """
        Returns the budget type
        """
        if self._data:
            return self._data['budgetMetaData']['budgetType']

    @property
    def currency_locale(self):
        """
        Returns the budget's currency locale
        """
        if self._data:
            return self._data['budgetMetaData']['currencyLocale']

    @property
    def date_locale(self):
        """
        Returns the budget's date locale
        """
        if self._data:
            return self._data['budgetMetaData']['dateLocale']

    @property
    def accounts(self):
        """
        Returns all the accounts stored in the Budget
        """
        if not hasattr(self, '_accounts'):
            self._accounts = EntityList([Account(self, account) for account in self._data['accounts']])
        return self._accounts

    @property
    def payees(self):
        if not hasattr(self, '_payees'):
            self._payees = EntityList([Entity(self, payee) for payee in self._data['payees']])
        return self._payees


    @property
    def transactions(self):
        if not hasattr(self, '_transactions'):
            self._transactions = EntityList([Entity(self, transaction) for transaction in self._data['transactions']])
        return self._transactions