from rest_framework import serializers

from apps.catalog.models import Size, Color, Category, Catalog, Specification
from apps.files.models import File
from apps.files.serializer import FileSerializer


class GetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id',
                  'name']


class MultiLanguageCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id',
                  'name_uz',
                  'name_ru',
                  'name_en', ]


class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name_uz',
                  'name_ru',
                  'name_en', ]


class GetColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id',
                  'name']


class PostColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id',
                  'name_uz',
                  'name_ru',
                  'name_en', ]


class GetSizeSerializer(serializers.ModelSerializer):
    size_type_display = serializers.CharField(source='get_size_type_display', read_only=True)

    class Meta:
        model = Size
        fields = ['id',
                  'name',
                  'size_type',
                  'size_type_display', ]


class PostSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id',
                  'name_uz',
                  'name_ru',
                  'name_en',
                  'size_type', ]


class GetCatalogSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, read_only=True, required=False, allow_null=True)
    category = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Catalog
        fields = ['id',
                  'name',
                  'description',
                  'files',
                  'shape',
                  'material',
                  'category', ]


class GetSpecificationSerializer(serializers.ModelSerializer):
    miniature = serializers.CharField(source='miniature.path', allow_null=True)
    catalog = serializers.CharField(source='catalog.name')
    size = GetSizeSerializer(many=True, allow_null=True)
    color = serializers.CharField(source='color.name')
    files = FileSerializer(many=True, read_only=True, required=False, allow_null=True)

    class Meta:
        model = Specification
        fields = ['id',
                  'is_active',
                  'vendor_code',
                  'price',
                  'discount',
                  'miniature',
                  'catalog',
                  'size',
                  'color',
                  'files', ]


class PostSpecificationSerializer(serializers.ModelSerializer):
    files = serializers.SlugRelatedField(slug_field='id', many=True, queryset=File.objects.all())
    size = serializers.SlugRelatedField(slug_field='id', many=True, queryset=Size.objects.all())

    class Meta:
        model = Specification
        fields = ['id',
                  'is_active',
                  'vendor_code',
                  'price',
                  'discount',
                  'miniature',
                  'catalog',
                  'size',
                  'color',
                  'files', ]


class InsideCatalogSpecificationSerializer(serializers.ModelSerializer):
    files = serializers.SlugRelatedField(slug_field='id', many=True, queryset=File.objects.all())
    size = serializers.SlugRelatedField(slug_field='id', many=True, queryset=Size.objects.all())

    class Meta:
        model = Specification
        fields = ['id',
                  'is_active',
                  'vendor_code',
                  'price',
                  'discount',
                  'miniature',
                  'size',
                  'color',
                  'files', ]


class ProductSpecificationSerializer(serializers.ModelSerializer):
    miniature = FileSerializer(many=True, read_only=True, required=False, allow_null=True)
    color = serializers.CharField(source='color.name')
    size = GetSizeSerializer(many=True, allow_null=True)

    class Meta:
        model = Specification
        fields = ['price',
                  'discount',
                  'color',
                  'size',
                  'vendor_code',
                  'miniature', ]


class SearchProductSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, read_only=True, required=False, allow_null=True)
    category = serializers.CharField(source='category.name')
    specs = ProductSpecificationSerializer(many=True, allow_null=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        active_specs = instance.specs.filter(is_active=True)
        representation['specs'] = ProductSpecificationSerializer(active_specs, many=True).data
        return representation

    class Meta:
        model = Catalog
        fields = ['id',
                  'name',
                  'description',
                  'files',
                  'category',
                  'specs', ]


class PostCatalogSerializer(serializers.ModelSerializer):
    files = serializers.SlugRelatedField(slug_field='id', many=True, queryset=File.objects.all())
    specs = InsideCatalogSpecificationSerializer(many=True)

    def create(self, validated_data):
        specs = validated_data.pop('specs', [])
        instance = super().create(validated_data)
        for spec in specs:
            if not spec.get('miniature'):
                spec.pop('miniature', '')
            spec_files = spec.pop('files', [])
            spec_sizes = spec.pop('size', [])
            specification = Specification.objects.create(catalog_id=instance.id, **spec)
            specification.files.add(*spec_files)
            specification.size.add(*spec_sizes)
            instance.specs.add(specification)
        return instance

    def update(self, instance, validated_data):
        specs = validated_data.pop('specs', [])
        instance: Catalog = super().update(instance, validated_data)
        instance.specs.all().delete()
        for spec in specs:
            if not spec.get('miniature'):
                spec.pop('miniature', '')
            spec_files = spec.pop('files', [])
            spec_sizes = spec.pop('size', [])
            specification = Specification.objects.create(catalog_id=instance.id, **spec)
            specification.files.add(*spec_files)
            specification.size.add(*spec_sizes)
            instance.specs.add(specification)
        return instance

    class Meta:
        model = Catalog
        fields = [
            'id',
            'name_uz',
            'name_ru',
            'name_en',
            'description_uz',
            'description_ru',
            'description_en',
            'shape_uz',
            'shape_ru',
            'shape_en',
            'material_uz',
            'material_ru',
            'material_en',
            'files',
            'specs',
            'category', ]


class RetrieveCatalogSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, read_only=True, required=False, allow_null=True)
    category = MultiLanguageCategorySerializer(allow_null=True)
    specs = GetSpecificationSerializer(many=True, read_only=True)

    class Meta:
        model = Catalog
        fields = ['id',
                  'name_uz',
                  'name_ru',
                  'name_en',
                  'description_uz',
                  'description_ru',
                  'description_en',
                  'files',
                  'shape_uz',
                  'shape_ru',
                  'shape_en',
                  'material_uz',
                  'material_ru',
                  'material_en',
                  'category',
                  'specs', ]


class MultiLanguageCatalogSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, read_only=True, required=False, allow_null=True)
    category = MultiLanguageCategorySerializer(allow_null=True)
    specs = GetSpecificationSerializer(many=True, read_only=True)

    class Meta:
        model = Catalog
        fields = ['id',
                  'name_uz',
                  'name_ru',
                  'name_en',
                  'description_uz',
                  'description_ru',
                  'description_en',
                  'shape_uz',
                  'shape_ru',
                  'shape_en',
                  'material_uz',
                  'material_ru',
                  'material_en',
                  'specs',
                  'files',
                  'category', ]
