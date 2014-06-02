import click
from gandi.cli.core.conf import GandiContextHelper


class DatacenterParamType(click.Choice):
    name = 'datacenter'

    def __init__(self):
        gandi = GandiContextHelper()
        choices = [item['iso'] for item in gandi.datacenter.list()]
        self.choices = choices


class PaasTypeParamType(click.Choice):
    name = 'paas type'

    def __init__(self):
        gandi = GandiContextHelper()
        choices = [item['name'] for item in gandi.paas.type_list()]
        self.choices = choices


DATACENTER = DatacenterParamType()
PAAS_TYPE = PaasTypeParamType()
