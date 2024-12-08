from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer
import bleach

def sanitize_content(content):
    allowed_tags = ['b', 'i', 'u', 'em', 'strong', 'a']
    allowed_attributes = {'a': ['href', 'title']}
    return bleach.clean(content, tags=allowed_tags, attributes=allowed_attributes)

class ProductPostAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permissions_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        title = request.data.get('title')
        description = request.data.get('desc')
        
        # Sanitize title and description
        sanitized_title = sanitize_content(title)
        sanitized_description = sanitize_content(description)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Save the sanitized data
            serializer.save(title=sanitized_title, desc=sanitized_description)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetAllProductsAPIView(generics.ListAPIView):
	products = Product.objects.all()
	serializer_class = ProductSerializer
	permission_classes = (IsAuthenticated)

	def get(self, products):
		return Response(products, status=status.HTTP_200_OK)
	
class GetProductByIdAPIView(generics.RetrieveAPIView):
	permission_classes = (IsAuthenticated)
	serializer_class = ProductSerializer

	def get(self, pd_id, user_id):
		try:
			product = Product.objects.get(id=pd_id, user_id=user_id)
			return Response(product, status=status.HTTP_200_OK)
		except Product.DoesNotExist:
			return None
		
class UpdateProductByIdAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer

    def put(self, request, pd_id, *args, **kwargs):
        product_instance = Product.objects.get(id=pd_id, user_id=request.user.id)
        if not product_instance:
            return Response({"message": "No product exists"}, status=status.HTTP_400_BAD_REQUEST)

        new_data = {
            "title": sanitize_content(request.data.get("title")),
            "desc": sanitize_content(request.data.get("desc")),
            "price": request.data.get("price"),
            "img": request.data.get("img")
        }
        product = ProductSerializer(instance=product_instance, data=new_data, partial=True)
        if product.is_valid():
            product.save()
            return Response(product.data, status=status.HTTP_200_OK)
        return Response(product.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteProductByIdAPIView(generics.DestroyAPIView):
	permission_classes = (IsAuthenticated)
	serializer_class = ProductSerializer

	def delete(self, request, pd_id, *args, **kwargs):
		product_ins = Product.objects.get(id=pd_id, user_id=request.user.id)
		if not product_ins:
			return Response({"message": "Object does not exists"}, status=status.HTTP_404_NOT_FOUND)
		product_ins.delete()
		return Response({"message": "Object is deleted"}, status=status.HTTP_200_OK)
