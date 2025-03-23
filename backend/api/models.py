# backend/api/models.py
from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from decimal import Decimal


class Quan(models.Model):
    """District entity"""
    ten_quan = models.CharField(max_length=50, verbose_name="Tên Quận")

    class Meta:
        verbose_name = "Quận"
        verbose_name_plural = "Quận"

    def __str__(self):
        return self.ten_quan


class LoaiDaiLy(models.Model):
    """Distributor Type entity"""
    ten_loai_dai_ly = models.CharField(max_length=50, verbose_name="Tên Loại Đại Lý")
    no_toi_da = models.DecimalField(
        max_digits=18,
        decimal_places=0,
        verbose_name="Nợ Tối Đa",
        validators=[MinValueValidator(Decimal('0'))]
    )

    class Meta:
        verbose_name = "Loại Đại Lý"
        verbose_name_plural = "Loại Đại Lý"

    def __str__(self):
        return self.ten_loai_dai_ly


class DaiLy(models.Model):
    """Distributor entity"""
    ten_dai_ly = models.CharField(max_length=100, verbose_name="Tên Đại Lý")
    dien_thoai = models.CharField(
        max_length=20,
        verbose_name="Điện Thoại",
        validators=[
            RegexValidator(
                regex=r'^\d{10,11}$',
                message="Số điện thoại phải có 10-11 chữ số."
            )
        ]
    )
    dia_chi = models.CharField(max_length=200, verbose_name="Địa Chỉ")
    quan = models.ForeignKey(
        Quan,
        on_delete=models.PROTECT,
        verbose_name="Quận",
        related_name="dai_lys"
    )
    loai_dai_ly = models.ForeignKey(
        LoaiDaiLy,
        on_delete=models.PROTECT,
        verbose_name="Loại Đại Lý",
        related_name="dai_lys"
    )
    ngay_tiep_nhan = models.DateField(verbose_name="Ngày Tiếp Nhận", auto_now_add=True)
    email = models.EmailField(max_length=100, blank=True, null=True, verbose_name="Email")
    tien_no = models.DecimalField(
        max_digits=18,
        decimal_places=0,
        default=0,
        verbose_name="Tiền Nợ",
        validators=[MinValueValidator(Decimal('0'))]
    )

    class Meta:
        verbose_name = "Đại Lý"
        verbose_name_plural = "Đại Lý"

    def __str__(self):
        return self.ten_dai_ly

    def save(self, *args, **kwargs):
        # Kiểm tra ràng buộc khi lưu đại lý
        if self.tien_no > self.loai_dai_ly.no_toi_da:
            raise ValueError(f"Tiền nợ vượt quá mức tối đa cho phép ({self.loai_dai_ly.no_toi_da})")

        # Kiểm tra số lượng đại lý trong quận
        if not self.pk:  # Chỉ kiểm tra khi tạo mới
            quy_dinh = QuyDinh.objects.filter(ten_quy_dinh="SoDaiLyToiDaTrongQuan").first()
            if quy_dinh:
                so_toi_da = int(quy_dinh.gia_tri)
                so_daily_hien_tai = DaiLy.objects.filter(quan=self.quan).count()
                if so_daily_hien_tai >= so_toi_da:
                    raise ValueError(f"Quận đã đạt số lượng đại lý tối đa ({so_toi_da})")

        super().save(*args, **kwargs)


class QuyDinh(models.Model):
    """Regulation entity"""
    ten_quy_dinh = models.CharField(max_length=100, verbose_name="Tên Quy Định", unique=True)
    gia_tri = models.CharField(max_length=4000, verbose_name="Giá Trị")
    mo_ta = models.TextField(blank=True, null=True, verbose_name="Mô Tả")

    class Meta:
        verbose_name = "Quy Định"
        verbose_name_plural = "Quy Định"

    def __str__(self):
        return self.ten_quy_dinh