import os
from json import load
import locale
from pynab.exceptions import InvalidBudget


class Category(object):
    pass


class Account(dict):

    @property
    def id(self):
        return self['entityId']

    @property
    def name(self):
        return self['name']

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

    def __repr__(self):
        return u'<{}>'.format(self.__unicode__())


class Budget(object):

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

    @property
    def budget_type(self):
        """
        Returnt the budget type
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
        return [Account(account) for account in self._data['accounts']]