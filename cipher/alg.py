import io
from base64 import b64decode, b64encode

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from PIL import Image

formatting = {
    "JPG": "JPEG",
    "JPEG": "JPEG",
    "PNG": "PNG"
}


class AES_ECB:
    def __init__(self):
        self.key = Random.new().read(AES.block_size)

    def encrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_ECB)
        return b64encode(cipher.encrypt(pad(data, AES.block_size))).decode(), self.key

    def decrypt(self, data, key):
        cipher = AES.new(key, AES.MODE_ECB)
        ciphertext = b64decode(data)
        return cipher.decrypt(ciphertext)


cipher = AES_ECB()


def encrypt_image(image_path, message):
    org_img = Image.open(image_path)
    org_pixelMap = org_img.load()
    enc_img = Image.new(org_img.mode, org_img.size)
    enc_pixelsMap = enc_img.load()

    message, key = cipher.encrypt(message.encode())
    msg_index = 0
    msg_len = len(message)

    for row in range(org_img.size[0]):
        for col in range(org_img.size[1]):
            list = org_pixelMap[row, col]
            r = list[0]  # R value
            g = list[1]  # G value
            b = list[2]  # B value

            if row == 0 and col == 0:
                ascii = msg_len
                enc_pixelsMap[row, col] = (ascii, g, b)
            elif msg_index <= msg_len:
                c = message[msg_index - 1]
                ascii = ord(c)
                enc_pixelsMap[row, col] = (ascii, g, b)
            else:
                enc_pixelsMap[row, col] = (r, g, b)
            msg_index += 1
    org_img.close()

    # enc_img.show()

    # Сохраняем изображение в буфере io.BytesIO()
    with io.BytesIO() as output:
        enc_img.save(output, format=formatting[
            image_path.split('.')[-1].upper()])  # Можно указать другой формат (PNG, BMP, etc.)
        output.seek(0)  # Переместить указатель на начало буфера
        image_buffer = output.read()  # Читаем данные из буфера

    enc_img.close()
    return image_buffer, key


def decrypt_image(image_path, key):
    enc_img = Image.open(image_path)
    enc_pixelMap = enc_img.load()

    message = ""
    msg_index = 0

    for row in range(enc_img.size[0]):
        for col in range(enc_img.size[1]):
            list = enc_pixelMap[row, col]
            r = list[0]  # R value

            if col == 0 and row == 0:
                msg_len = r
            elif msg_len > msg_index:
                message = message + chr(r)
                msg_index = msg_index + 1

    enc_img.close()

    if message:
        message = cipher.decrypt(message, key)

    return message.decode()


if __name__ == "__main__":
    image_path = 'bug_genshin_fontain.png'
    message = "Hi Joni, my secret it's flag{th1s_test_f1ag}"
    image_buffer, key = encrypt_image(image_path, message)

    image_path = 'encrypted_image.png'
    message = decrypt_image(image_path, key)
    print(message)


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = ImageCipherApp()
#     ex.show()
#     sys.exit(app.exec_())
