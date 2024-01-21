from rest_framework import serializers
from ..models import Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        # Specify the fields used by serializer
        fields = [
            'age',
            'body_mass_index',
            'spo2',
            'dayshome',
            'gender',
            'f_test_ex',
            'f_test_in',
            'comorb_ccc',
            'comorb_bl',
            'cd_ozhir',
            'comorb_all',
            'l_109',
            'lf',
            'rox',
            'spo2_fio',
            'ch_d',
        ]