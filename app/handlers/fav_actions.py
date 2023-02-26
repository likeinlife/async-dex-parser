from pathlib import Path
import json
import pyperclip

class FavouriteList:
    BASEPATH = Path(__file__).parent.parent / 'favs.json'

    def __call__(self, args):
        action = args.action
        table = {
            'list': self.list,
            'add': self.add,
            'del': self.delete,
        }
        return table[action](args)

    def checkFavListIsEmpty(self):
        global abs_path_to_fav
        if self.BASEPATH.exists():
            if self.BASEPATH.__sizeof__():
                return False
        else:
            with open(self.BASEPATH, 'w', encoding='UTF-8') as file_obj:
                json.dump({}, file_obj, ensure_ascii=False, indent=4)
            print('Favourite list does not exists. Just made one')

        return True

    def list(self, _):
        if self.checkFavListIsEmpty():
            return
        with open(self.BASEPATH, 'r') as file_obj:
            favs = json.load(file_obj)

        for number, (title_id, title_name) in enumerate(favs.items()):
            print(f'{number: >3} | {title_id} | {title_name}')

        copy = input('Copy? y/n ')
        if copy == 'n':
            return
        chapter_number = int(input('chapter number? >> '))
        for number, (title_id, title_name) in enumerate(favs.items()):
            if number == chapter_number:
                pyperclip.copy(title_id)

    def add(self, args):
        title = {args.title: args.id}
        if self.checkFavListIsEmpty():
            with open(self.BASEPATH, 'w') as file_obj:
                json.dump(title, file_obj, indent=4, ensure_ascii=False)
                return

        with open(self.BASEPATH, 'r') as file_obj:
            favourites: dict = json.load(file_obj)
            favourites.update(title)

        with open(self.BASEPATH, 'w') as file_obj:
            json.dump(favourites, file_obj, ensure_ascii=False, indent=4)

        print(f'Add {args.title}')

    def delete(self, args):
        with open(self.BASEPATH, 'r') as file_obj:
            favourites: dict = json.load(file_obj)

        if args.id in favourites:
            favourites.pop(args.id)
            print(f"deleted {args.id}")
        else:
            print("Element not found")
            return

        with open(self.BASEPATH, 'w') as file_obj:
            json.dump(favourites, file_obj)
            return
