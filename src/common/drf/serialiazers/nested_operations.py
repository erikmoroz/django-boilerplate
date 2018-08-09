class NestedOperationsMixin(object):
    def first_or_create(self, model, data):
        obj = model.objects.filter(**data).first()
        if not obj:
            obj = model.objects.create(**data)
        return obj

    def replace_fk(self, item, fk_mapping, search_existing=True):
        if not fk_mapping:
            return item

        for fk, fk_model in fk_mapping.items():
            if fk in item:
                item[fk] = self.first_or_create(fk_model, item[fk]) if search_existing else fk_model.objects.create(
                    **item[fk])

        return item

    def create_nested(self, data, model, extra_fields, fk_mapping=None, search_existing=True):
        items = []
        for item in data:
            item = self.replace_fk(item, fk_mapping, search_existing)
            obj = model(**item, **extra_fields)
            items.append(obj)
        model.objects.bulk_create(items)

    def update_nested(self, data, model, queryset, extra_fields, fk_mapping=None, pk_field='id', search_existing=True):
        create_items = []
        update_items = []

        for item in data:
            item = self.replace_fk(item, fk_mapping, search_existing)

            if pk_field in item:
                update_items.append(item)
            else:
                create_items.append(item)

        existing_ids = queryset.all().values_list(pk_field, flat=True)
        left_ids = [x[pk_field] for x in update_items]
        delete_items = list(set(existing_ids) - set(left_ids))

        # delete
        model.objects.filter(**{pk_field + '__in': delete_items}).delete()

        # update
        for item in update_items:
            pk = item[pk_field]
            del item[pk_field]

            if pk not in existing_ids:
                create_items.append(item)
                continue

            model.objects.filter(**{pk_field: pk}).update(**item)

        # create
        model.objects.bulk_create([model(**item, **extra_fields) for item in create_items])
