import csv, io
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import permission_required
from .models import *
from rest_framework import viewsets
from .serializers import *
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
fs = FileSystemStorage(location='tmp/')


# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['POST'])
    def upload_product(self, request):
        print("==================================")
        print(request)
        filename = request.FILES['filename']

        content = filename.read()
        file_content = ContentFile(content)
        file_name = fs.save(
            "_tmp.csv", file_content
        )

        tmp_file = fs.path(file_name)
        csv_file = open(tmp_file, errors="ignore")
        reader = csv.reader(csv_file)
        next(reader)

        product_list = []
        for id_, row in enumerate(reader):
            (
                p_name,
                price

            ) = row

            product_list.append(
                Product(
                    p_name=p_name,
                    price=price
                )
            )
        Product.objects.bulk_create(product_list)

        return Response("Success Fully uploaded data")


@permission_required('admin.can_add_log_entry')
def product_download(request):
    items = Product.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename="product.csv"'

    writer = csv.writer(response, delimiter=',')
    writer.writerow(['p_name', 'price'])

    for obj in items:
        writer.writerow([obj.p_name, obj.price])
    return response
