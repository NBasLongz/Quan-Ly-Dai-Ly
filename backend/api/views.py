# backend/api/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count
from .models import Quan, LoaiDaiLy, DaiLy, QuyDinh
from .serializers import QuanSerializer, LoaiDaiLySerializer, DaiLySerializer, QuyDinhSerializer


class QuanViewSet(viewsets.ModelViewSet):
    queryset = Quan.objects.all()
    serializer_class = QuanSerializer

    @action(detail=True, methods=['get'])
    def dai_lys(self, request, pk=None):
        """Lấy danh sách đại lý thuộc quận"""
        quan = self.get_object()
        dai_lys = DaiLy.objects.filter(quan=quan)
        serializer = DaiLySerializer(dai_lys, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def count_daily(self, request):
        """Lấy số lượng đại lý theo quận"""
        quans = Quan.objects.annotate(so_daily=Count('dai_lys'))
        data = [{
            'id': quan.id,
            'ten_quan': quan.ten_quan,
            'so_daily': quan.so_daily
        } for quan in quans]
        return Response(data)

    def destroy(self, request, *args, **kwargs):
        """Ghi đè phương thức xóa để kiểm tra ràng buộc"""
        quan = self.get_object()
        if quan.dai_lys.exists():
            return Response(
                {"error": "Không thể xóa quận có đại lý"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)


class LoaiDaiLyViewSet(viewsets.ModelViewSet):
    queryset = LoaiDaiLy.objects.all()
    serializer_class = LoaiDaiLySerializer

    @action(detail=True, methods=['get'])
    def dai_lys(self, request, pk=None):
        """Lấy danh sách đại lý thuộc loại đại lý"""
        loai = self.get_object()
        dai_lys = DaiLy.objects.filter(loai_dai_ly=loai)
        serializer = DaiLySerializer(dai_lys, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """Ghi đè phương thức cập nhật để kiểm tra ràng buộc"""
        instance = self.get_object()
        no_toi_da_moi = request.data.get('no_toi_da')

        # Kiểm tra nếu no_toi_da mới nhỏ hơn no_toi_da hiện tại
        if no_toi_da_moi and float(no_toi_da_moi) < float(instance.no_toi_da):
            # Kiểm tra các đại lý hiện tại
            dai_lys_vuot_qua = DaiLy.objects.filter(
                loai_dai_ly=instance,
                tien_no__gt=no_toi_da_moi
            )
            if dai_lys_vuot_qua.exists():
                return Response(
                    {"error": "Có đại lý có nợ vượt quá mức nợ tối đa mới"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Ghi đè phương thức xóa để kiểm tra ràng buộc"""
        loai = self.get_object()
        if loai.dai_lys.exists():
            return Response(
                {"error": "Không thể xóa loại đại lý đang được sử dụng"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)


class DaiLyViewSet(viewsets.ModelViewSet):
    queryset = DaiLy.objects.all()
    serializer_class = DaiLySerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Tìm kiếm đại lý"""
        keyword = request.query_params.get('keyword', '')
        if keyword:
            dai_lys = DaiLy.objects.filter(
                Q(ten_dai_ly__icontains=keyword) |
                Q(dien_thoai__icontains=keyword) |
                Q(dia_chi__icontains=keyword) |
                Q(email__icontains=keyword)
            )
            serializer = DaiLySerializer(dai_lys, many=True)
            return Response(serializer.data)
        return Response([])

    def create(self, request, *args, **kwargs):
        """Ghi đè phương thức tạo mới để xử lý lỗi ràng buộc"""
        try:
            return super().create(request, *args, **kwargs)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """Ghi đè phương thức cập nhật để xử lý lỗi ràng buộc"""
        try:
            return super().update(request, *args, **kwargs)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """Ghi đè phương thức xóa để kiểm tra ràng buộc"""
        dai_ly = self.get_object()
        if dai_ly.tien_no > 0:
            return Response(
                {"error": "Không thể xóa đại lý còn nợ"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)


class QuyDinhViewSet(viewsets.ModelViewSet):
    queryset = QuyDinh.objects.all()
    serializer_class = QuyDinhSerializer

    @action(detail=False, methods=['get'])
    def by_name(self, request):
        """Lấy quy định theo tên"""
        name = request.query_params.get('name', '')
        if name:
            try:
                quy_dinh = QuyDinh.objects.get(ten_quy_dinh=name)
                serializer = QuyDinhSerializer(quy_dinh)
                return Response(serializer.data)
            except QuyDinh.DoesNotExist:
                return Response({"error": "Quy định không tồn tại"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Thiếu tên quy định"}, status=status.HTTP_400_BAD_REQUEST)


