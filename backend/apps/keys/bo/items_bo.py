from apps.keys.models import KeyItem, Folder

class FolderBO:
    @staticmethod
    def create_folder(user, name):
        return Folder.objects.create(user=user, name=name)

    @staticmethod
    def list_folders(user):
        return Folder.objects.filter(user=user)

    @staticmethod
    def update_folder(instance, **data):
        for attr, value in data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    @staticmethod
    def delete_folder(instance):
        instance.delete()

class ItemsBO:
    @staticmethod
    def create_item(user, **data):
        return KeyItem.objects.create(user=user, **data)

    @staticmethod
    def list_items(user):
        return KeyItem.objects.filter(user=user)

    @staticmethod
    def update_item(instance, **data):
        for attr, value in data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    @staticmethod
    def delete_item(instance):
        instance.delete()

    @staticmethod
    def get_organized_keys(user):
        """
        Retorna las keys organizadas por carpetas y las keys sin carpeta.
        """
        folders = Folder.objects.filter(user=user).prefetch_related('items')
        keys_without_folder = KeyItem.objects.filter(user=user, folder__isnull=True)
        
        return {
            'folders': folders,
            'items': keys_without_folder
        }
