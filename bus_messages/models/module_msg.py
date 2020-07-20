from django.db import models
import datetime

class ModuleMsg(models.Model):
    protocol_id = models.CharField(max_length=3)
    message_type = models.CharField(max_length=1)
    message_length = models.IntegerField()
    message_id = models.CharField(max_length=255)
    string_id = models.CharField(max_length=2)
    module_id = models.CharField(db_index=True, max_length=2)
    state = models.CharField(max_length=1)
    state_of_change = models.IntegerField()
    min_cell_temperature = models.IntegerField()
    avg_cell_temperature = models.IntegerField()
    max_cell_temperature = models.IntegerField()
    voltage = models.IntegerField()
    min_cell_voltage = models.IntegerField()
    avg_cell_voltage = models.IntegerField()
    max_cell_voltage = models.IntegerField()
    amperes = models.IntegerField()
    alarm_and_status = models.BigIntegerField()
    assembly_revision = models.CharField(max_length=4)
    serial_no = models.CharField(db_index=True, max_length=16)
    main_software_version = models.CharField(max_length=4)
    subordinate_software_version = models.CharField(max_length=4)
    max_front_power_conn_temp = models.IntegerField()

    # Flags
    temperature_warning = models.BooleanField(default=False)
    temperature_fault = models.BooleanField(default=False)
    high_current_warning = models.BooleanField(default=False)
    high_current_fault = models.BooleanField(default=False)
    high_voltage_warning = models.BooleanField(default=False)
    high_voltage_fault = models.BooleanField(default=False)
    low_voltage_warning = models.BooleanField(default=False)
    low_voltage_fault = models.BooleanField(default=False)
    low_voltage_non_recoverable_fault = models.BooleanField(default=False)
    charge_low_warning = models.BooleanField(default=False)
    communication_error = models.BooleanField(default=False)
    communication_fault = models.BooleanField(default=False)
    under_volt_disable = models.BooleanField(default=False)
    over_volt_disable = models.BooleanField(default=False)
    cell_0_balancing = models.BooleanField(default=False)
    cell_1_balancing = models.BooleanField(default=False)
    cell_2_balancing = models.BooleanField(default=False)
    cell_3_balancing = models.BooleanField(default=False)
    cell_4_balancing = models.BooleanField(default=False)
    cell_5_balancing = models.BooleanField(default=False)
    cell_6_balancing = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    SAMPLE_DATA = {
        'protocol_id': '001',
        'message_type': 'M',
        'message_length': '122',
        'message_id': '419',
        'string_id': '00',
        'module_id': '00',
        'state': 'R',
        'state_of_change': '051',
        'min_cell_temperature': '022',
        'avg_cell_temperature': '023',
        'max_cell_temperature': '027',
        'voltage': '025709',
        'min_cell_voltage': '003653',
        'avg_cell_voltage': '003672',
        'max_cell_voltage': '003710',
        'amperes': '00000',
        'alarm_and_status': '80000000', # Temperature Fault only
        'assembly_revision': '000',
        'serial_no': '1311250000800',
        'main_software_version': '0501',
        'subordinate_software_version': '0496',
        'max_front_power_conn_temp': '029'
    }

    def url(self):
        return "/module/" + self.serial_no

    def to_dict(self):
        attributes = self.__dict__
        attributes.pop('_state')
        return {**attributes, **{'url': self.url()}}

    @classmethod
    def serial_numbers(cls):
        return list(map((lambda serial: serial['serial_no']), cls.objects.values('serial_no').distinct()))

    @classmethod
    def latest_for_serial(cls, serial):
        return cls.objects.filter(serial_no=serial).latest('created_at')

    @classmethod
    def last_24_hours(cls, serial):
        cutoff = datetime.datetime.now() - datetime.timedelta(hours=24)
        return cls.objects.filter(serial_no=serial).filter(created_at__gte=cutoff)

    @classmethod
    def latest_messages(cls):
        return list(map((lambda serial: cls.latest_for_serial(serial).to_dict()), cls.serial_numbers()))
