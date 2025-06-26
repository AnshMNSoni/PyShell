import os

class BulkRenamer:
    @staticmethod
    def bulk_rename(path,prefix='',suffix='',replace_from='',replace_to='', number=False, new_extension=''):
        try:
            file = os.listdir(path)
            count = 1

            for filename in file:
                old_path = os.path.join(path,filename)

                if os.path.isfile(old_path):
                    name, ext = os.path.splitext(filename)

                name = name.replace(replace_from,replace_to)

                if number:
                    new_name = f"{prefix}{count}{suffix}"
                else:
                    new_name = f"{prefix}{suffix}"

                ext = new_extension if new_extension else ext  

                final_name = f"{new_name}{ext}"
                final_path = os.path.join(path, final_name)
                os.rename(old_path,final_path)

                print(f"renamed:{filename} to {final_name}")
                count += 1

        except Exception as e:
            
            print(f"error:{e}")
