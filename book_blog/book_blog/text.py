import random

hack_message = [
    "Hack được hôm nay, nhưng đời không có nút xóa lịch sử đâu 😌.",
    "Biết bạn “tày” rồi nên đừng Ctrl + Shift + C hay F12 đi, OK?",
    "Giỏi mà đi hack thì phí lắm, dùng lượng IQ đấy làm gì đó cho đời nha.🫰🏻",
    "Thông minh lắm, dám hack cơ đấy. Đúng là con trai của ta, hahaha😏",
    "Bạn khá lắm, chúc bạn ... may mắn lần sau...",
    "Ối dồi ôi!🎵Ối dồi ôi!🎵Trình là gì mà là trầm ai chínhhhh ♩♪♪♪♩♪♩.",
    "Đứng ở dưới đất nhảy mạnh lên.♩ Ai hack thì đi về.♪ Phonk crack,♪ Phonk crack,♪ Phonk crack,♪ Phonk crack,♪"
    "Anh hẹn em HackerBall.🎵 Ta vờn nhau HackerBall.🎵 Tay vợt bên dưới hông.🎵 Anh đập banh,🎵 đập banh.🎵 Đến em mạnh vào.🎵"
]

def return_for_hacker():
    """
    Hàm để "bắn tùm lum, bắn tung tóe" đạo lí vào mặt mấy thằng hacker...
    Well, 67?
    """
    return hack_message[random.randint(0, len(hack_message) - 1)]



def get_id_number_shuffle(out_id):
    """
    Hủy xáo ID
    """
    num = 138432 - (out_id - 853647)/5
    return num