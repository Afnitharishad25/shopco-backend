from django.shortcuts import render

# Create your views here.
from django.db.models import Q
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer


class ProductListCreateView(generics.ListCreateAPIView):
    
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()

        search_query = self.request.query_params.get("search", "").strip()

        if search_query:
           queryset = queryset.filter(
                Q(name__icontains=search_query)
                | Q(category__icontains=search_query)
                | Q(dress_style__icontains=search_query)
                | Q(description__icontains=search_query)
            )
        return queryset



class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer