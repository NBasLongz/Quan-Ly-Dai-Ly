# backend/api/serializers.py
from rest_framework import serializers
from .models import Quan, LoaiDaiLy, DaiLy, QuyDinh


class QuanSerializer(serializers.ModelSerializer):
    so_dai_ly = serializers.SerializerMethodField()

    class Meta:
        model = Quan
        fields = ['id', 'ten_quan', 'so_dai_ly']

    def get_so_dai_ly(self, obj):
        return obj.dai_lys.count()


class LoaiDaiLySerializer(serializers.ModelSerializer):
    so_dai_ly = serializers.SerializerMethodField()

    class Meta:
        model = LoaiDaiLy
        fields = ['id', 'ten_loai_dai_ly', 'no_toi_da', 'so_dai_ly']

    def get_so_dai_ly(self, obj):
        return obj.dai_lys.count()


class DaiLySerializer(serializers.ModelSerializer):
    ten_quan = serializers.ReadOnlyField(source='quan.ten_quan')
    ten_loai_dai_ly = serializers.ReadOnlyField(source='loai_dai_ly.ten_loai_dai_ly')

    class Meta:
        model = DaiLy
        fields = [
            'id', 'ten_dai_ly', 'dien_thoai', 'dia_chi',
            'quan', 'ten_quan', 'loai_dai_ly', 'ten_loai_dai_ly',
            'ngay_tiep_nhan', 'email', 'tien_no'
        ]
        read_only_fields = ['ngay_tiep_nhan']


class QuyDinhSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuyDinh
        fields = ['id', 'ten_quy_dinh', 'gia_tri', 'mo_ta']