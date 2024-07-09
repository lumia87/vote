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
user.save()
# Nang cap nguoi dung thanh staff (de co quyen admin)
user = CustomUser.objects.get(username='hanb')  # Thay 'username_cua_ban' bằng tên đăng nhập của người dùng
user.is_staff = True
user.save()

user1 = CustomUser.objects.create_user(username='gk1', email='gk1@gmail.com', full_name='gk1', password='888889', bypass_otp=True)
user2 = CustomUser.objects.create_user(username='gk2', email='gk2@gmail.com', full_name='gk2', password='888889', bypass_otp=True)
user3 = CustomUser.objects.create_user(username='gk3', email='gk3@gmail.com', full_name='gk3', password='888889', bypass_otp=True)

user1.save()
user2.save()
user3.save()



# Them Contestant
python manage.py shell
from datetime import date
from vote_app2.models import Contestant  # Thay thế 'vote_app2' bằng tên ứng dụng của bạn

# Tạo một instance mới của Contestant


ts2 = Contestant(
    full_name='ts2',
    date_of_birth=date(1990, 5, 15),
    email='ts2@gmail.com',
)
ts2=Contestant.objects.get(email='ts2@gmail.com')
ts2.set_password('888889')  # Sử dụng set_password để hash mật khẩu

Khi tao bang cach tren thi khong dang nhap thanh cong
python manage.py shell
from datetime import date
from vote_app2.models import Contestant  # Thay thế 'vote_app2' bằng tên ứng dụng của bạn
ts1=Contestant.objects.create_contestant(full_name='ts1', date_of_birth=date(1990, 5, 15),email='ts1@gmail.com', password='888889', bypass_otp=True) 
ts2=Contestant.objects.create_contestant(full_name='ts2', date_of_birth=date(1990, 5, 15),email='ts2@gmail.com', password='888889', bypass_otp=True) 
ts3=Contestant.objects.create_contestant(full_name='ts3', date_of_birth=date(1990, 5, 15),email='ts3@gmail.com', password='888889', bypass_otp=True) 

# Lưu instance vào cơ sở dữ liệu
ts1.save()
ts2.save()
ts3.save()

# Sua doi password cua contestant
ts1=Contestant.objects.get(email='ts1@gmail.com')
ts1.set_password('888889')  # Sử dụng set_password để hash mật khẩu

# Xoa cac Contestant
from vote_app2.models import Contestant  # Thay thế 'vote_app2' bằng tên ứng dụng của bạn
Contestant.objects.all().delete()

# Lay 1 phan tu
from vote_app2.models import Contestant  # Thay thế 'vote_app2' bằng tên ứng dụng của bạn
c= Contestant.objects.get(email='ts1@gmail.com')
c.email
c.password #Hien thi thong tin
# In ra để xác nhận đã tạo thành công
print(ts1, ts2, ts3)



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

# Note
USERNAME_FIELD và REQUIRED_FIELDS là các thuộc tính trong lớp AbstractBaseUser của Django, được sử dụng để tùy chỉnh mô hình người dùng trong ứng dụng. Dưới đây là mô tả chi tiết và cách sử dụng chúng:

**USERNAME_FIELD**
Mô tả: USERNAME_FIELD xác định trường nào sẽ được sử dụng để xác thực người dùng. Mặc định, Django sử dụng trường username, nhưng bạn có thể thay đổi trường này thành một trường khác như email.
Cách sử dụng: Khi bạn tạo một lớp người dùng tùy chỉnh, bạn có thể đặt USERNAME_FIELD để chỉ định trường sẽ được sử dụng cho việc đăng nhập.

**REQUIRED_FIELDS**
Mô tả: REQUIRED_FIELDS là danh sách các trường bắt buộc khác (ngoài USERNAME_FIELD) cần thiết khi tạo một người dùng mới thông qua lệnh quản lý **createsuperuser.**
Cách sử dụng: Khi bạn định nghĩa mô hình người dùng tùy chỉnh, bạn liệt kê các trường bắt buộc vào REQUIRED_FIELDS. 
**Lưu ý** rằng USERNAME_FIELD không nên có trong REQUIRED_FIELDS.

**{% include %}**
o sánh chi tiết
Mục đích:

{% include %}: Nhúng nội dung của một template vào một template khác.
{% extends %}: Kế thừa và ghi đè các block từ một template khác.
Phạm vi sử dụng:

{% include %}: Tái sử dụng các thành phần nhỏ và độc lập của giao diện.
{% extends %}: Tạo cấu trúc layout chung cho nhiều trang và cho phép ghi đè các phần tử cụ thể trong template con.
Khả năng ghi đè:

{% include %}: Không có khả năng ghi đè các block; chỉ đơn giản là nhúng nội dung.
{% extends %}: Có khả năng ghi đè các block được định nghĩa trong template cha.
Quản lý template:

{% include %}: Giúp tái sử dụng các thành phần nhỏ mà không cần tạo ra một cấu trúc kế thừa.
{% extends %}: Giúp tạo ra một cấu trúc layout nhất quán và dễ quản lý cho các trang web phức tạp.

**AbstractUser trong Django là một lớp mô hình người dùng trừu tượng có sẵn những trường cơ bản sau:**
username: CharField để lưu trữ tên người dùng. Mặc định là một trường bắt buộc và duy nhất.
first_name: CharField để lưu trữ tên của người dùng.
last_name: CharField để lưu trữ họ của người dùng.
email: EmailField để lưu trữ địa chỉ email của người dùng. Mặc định là một trường bắt buộc và duy nhất.
password: CharField để lưu trữ mật khẩu của người dùng.
is_staff: BooleanField để xác định xem người dùng có quyền truy cập vào trang quản trị hay không.
is_active: BooleanField để xác định xem tài khoản người dùng có hoạt động hay không.
date_joined: DateTimeField để lưu trữ ngày và giờ người dùng được thêm vào hệ thống.
Ngoài các trường này, bạn cũng có thể mở rộng AbstractUser bằng cách thêm các trường tùy chỉnh thông qua việc kế thừa và mở rộng lớp mô hình này. Việc này cho phép bạn định nghĩa các trường bổ sung hoặc thay đổi các trường mặc định để phù hợp với yêu cầu cụ thể của dự án của bạn.

# Xu ly Migration bi xung dot
Migration bị xung đột: Đôi khi khi bạn thay đổi mô hình đã tồn tại, có thể xảy ra xung đột khi áp dụng migration. Trong trường hợp này, bạn có thể cần xóa hoặc sửa đổi các migration để phù hợp với cấu trúc hiện tại của database.

Xem danh sách migrations đã áp dụng: **python manage.py showmigrations**
Xóa migration không cần thiết: **python manage.py migrate vote_app2 zero**
Tạo migration: **python manage.py makemigrations vote_app2**
Áp dụng migration: **python manage.py migrate**