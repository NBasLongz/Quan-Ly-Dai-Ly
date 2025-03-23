# backend/api/admin.py
from django.contrib import admin
from .models import Quan, LoaiDaiLy, DaiLy, QuyDinh


@admin.register(Quan)
class QuanAdmin(admin.ModelAdmin):
    list_display = ('id', 'ten_quan', 'so_dai_ly')
    search_fields = ('ten_quan',)

    def so_dai_ly(self, obj):
        return obj.dai_lys.count()

    so_dai_ly.short_description = "Số đại lý"


@admin.register(LoaiDaiLy)
class LoaiDaiLyAdmin(admin.ModelAdmin):
    list_display = ('id', 'ten_loai_dai_ly', 'no_toi_da', 'so_dai_ly')
    search_fields = ('ten_loai_dai_ly',)

    def so_dai_ly(self, obj):
        return obj.dai_lys.count()

    so_dai_ly.short_description = "Số đại lý"


@admin.register(DaiLy)
class DaiLyAdmin(admin.ModelAdmin):
    list_display = ('id', 'ten_dai_ly', 'dien_thoai', 'quan', 'loai_dai_ly', 'ngay_tiep_nhan', 'tien_no')
    list_filter = ('quan', 'loai_dai_ly', 'ngay_tiep_nhan')
    search_fields = ('ten_dai_ly', 'dien_thoai', 'dia_chi', 'email')
    date_hierarchy = 'ngay_tiep_nhan'


@admin.register(QuyDinh)
class QuyDinhAdmin(admin.ModelAdmin):
    list_display = ('id', 'ten_quy_dinh', 'gia_tri', 'mo_ta')
    search_fields = ('ten_quy_dinh', 'mo_ta')