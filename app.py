import os
from flask import Flask, request, send_from_directory
from werkzeug.utils import secure_filename

# Папка для загрузки файлов
UPLOAD_FOLDER = "uploads"
# Разрешённые расширения файлов
ALLOWED_EXTENSIONS = {".zip", ".py", ".exe", ".js", ".java", ".cpp"}

# Создаём папку, если её нет
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Flask-приложение
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Проверка расширения файла
def allowed_file(filename):
    _, ext = os.path.splitext(filename)
    return ext.lower() in ALLOWED_EXTENSIONS


# Главная страница (форма загрузки)
@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files.get("file")
        name = request.form.get("name", "Аноним")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(save_path)
            return f"✅ Спасибо, {name}! Файл {filename} загружен.<br><a href='/'>Назад</a>"
        return "❌ Ошибка: неверный формат файла"
    
    return '''
    <h1>Загрузите свою программу</h1>
    <form method="post" enctype="multipart/form-data">
      Имя: <input type="text" name="name"><br><br>
      Файл: <input type="file" name="file"><br><br>
      <input type="submit" value="Отправить">
    </form>
    <br>
    <a href="/list">Посмотреть загруженные работы</a>
    '''


# Страница со списком файлов
@app.route("/list")
def list_files():
    files = os.listdir(app.config["UPLOAD_FOLDER"])
    if not files:
        return "<h1>Список загруженных работ</h1><p>Пока пусто.</p><br><a href='/'>Назад</a>"
    
    html = "<h1>Список загруженных работ</h1><ul>"
    for f in files:
        html += f"<li><a href='/download/{f}'>{f}</a></li>"
    html += "</ul><br><a href='/'>Назад</a>"
    return html


# Скачивание файла
@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)


# Запуск
if __name__ == "__main__":
    # host="0.0.0.0" нужен для Render
    app.run(host="0.0.0.0", port=8000)
