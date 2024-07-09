# Lay thong tin uuers

from vote_app2.models import CustomUser, Contestant
users = CustomUser.objects.all()
for user in users:
    print(f"Username: {user.username}, Is Staff: {user.is_staff}, Is Superuser: {user.is_superuser}")

# Lay thong tin Contestants va xoa tat ca
python manage.py shell
from vote_app2.models import Contestant
contestants = Contestant.objects.all()
print(contestants)
contestants.delete()

python manage.py dbshell
DROP TABLE vote_app2_contestant;

# Xoa tat ca du lieu trong sqlite3
python manage.py flush

# Them nguoi dung moi
python manage.py shell
from vote_app2.models import CustomUser
user = CustomUser.objects.create_user(username='hanb', email='nguyenbaha@gmail.com', full_name='Nguyen Ba Ha', password='888889', bypass_otp=True)
user2 = CustomUser.objects.create_user(username='test', email='test@gmail.com', full_name='test', password='888889', bypass_otp=True)
user3 = CustomUser.objects.create_user(username='nam', email='nam@gmail.com', full_name='Nam', password='888889', bypass_otp=True)

# Them Contestant
python manage.py shell
from datetime import date
from vote_app2.models import Contestant  # Thay thế 'vote_app2' bằng tên ứng dụng của bạn

# Tạo một instance mới của Contestant
contestant = Contestant(
    full_name='Nguyen Van A',
    date_of_birth=date(1990, 5, 15),
    position='TK',
)

# Lưu instance vào cơ sở dữ liệu
contestant.save()

# In ra để xác nhận đã tạo thành công
print(contestant)

# Chuyen nguoi dung thanh staff (de co quyen admin)
from vote_app2.models import CustomUser

user = CustomUser.objects.get(username='hanb')  # Thay 'username_cua_ban' bằng tên đăng nhập của người dùng
user.is_staff = True
user.save()



# Tạo người dùng mới
from vote_app2.models import CustomUser
user = CustomUser.objects.create_user(username='nguyenbaha@gmail.com', password='Linhchi87', email='nguyenbaha@gmail.com')
user.is_staff = True
user.save()

# Xóa tất cả các bản ghi Assignment

from vote_app2.models import Assignment

assignments = Assignment.objects.all()

assignments.delete()



# Lấy ra các bản ghi Assignment của một contestant cụ thể (ví dụ contestant_id=1)
from vote_app2.models import Assignment, Contestant
contestant = Contestant.objects.get(id=1)
assignments_to_delete = Assignment.objects.filter(contestant=contestant)

# Xóa các bản ghi Assignment đã lấy được
assignments_to_delete.delete()

