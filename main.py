from datetime import datetime
import cv2
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture  # добавляем импорт Texture
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
from os.path import sep


class VideoCamera(Image):
    def __init__(self, **kwargs):
        super(VideoCamera, self).__init__(**kwargs)
        self.capture = None
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self, dt):
        if not self.capture:
            self.capture = cv2.VideoCapture(0)
        ret, frame = self.capture.read()
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.texture = texture1


class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.layout1 = FloatLayout()

        self.video = VideoCamera()
        self.video.allow_stretch = True
        self.video.size_hint = (1, 1)
        self.layout1.add_widget(self.video)

        self.image = Image(source='', allow_stretch=True)
        self.image.pos_hint = {"x": 0, "y": 0}
        self.image.size_hint = (1, 1)
        self.image.opacity = 0
        self.layout1.add_widget(self.image)

        # Add the "Take Photo" button to the center of the app
        photo_button = Button(text='Сделать фото')
        photo_button.size_hint = (None, None)
        photo_button.size = (150, 50)
        photo_button.pos_hint = {"center_x": 0.5, "y": 0}
        photo_button.bind(on_press=self.take_photo)
        self.layout1.add_widget(photo_button)

        # Add the "Choose Image" button to the bottom-left of the app
        image_button = Button(markup=True, text='[size=20]Выбрать\nизображение[/size]')
        image_button.size_hint = (None, None)
        image_button.size = (150, 50)
        image_button.pos_hint = {"x": 0, "y": 0}
        image_button.bind(on_press=self.select_image)
        self.layout1.add_widget(image_button)

        layout.add_widget(self.layout1)

        return layout

    def select_image(self, instance):
        if platform == 'android':
            from android.permissions import request_permissions, Permission

            def callback(permissions, grant_results):
                if all([grant_result == Permission.GRANTED for grant_result in grant_results]):
                    self.open_file()

            request_permissions([Permission.READ_EXTERNAL_STORAGE], callback)
        else:
            self.open_file()

    def open_file(self):
        from tkinter import Tk
        from tkinter.filedialog import askopenfilename

        Tk().withdraw()
        filename = askopenfilename()

        if filename:
            self.image.source = filename
            self.image.reload()
            self.image.opacity = 0.5

        # Create and add the slider widget after an image is chosen
        if not hasattr(self, 'opacity_slider'):
            self.opacity_slider = Slider(min=0, max=1, value=0.5, step=0.01)
            self.opacity_slider.size_hint = (None, None)
            self.opacity_slider.size = (200, 50)
            self.opacity_slider.pos_hint = {"center_x": 0.5, "top": 1}
            self.opacity_slider.bind(value=self.change_opacity)
            self.layout1.add_widget(self.opacity_slider)

    def take_photo(self, instance):
        # Capture the current frame from the video camera and save it as an image
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'photo_{timestamp}.png'
        self.video.export_to_png(filename)

    def change_opacity(self, instance, value):
        self.image.opacity = value


if __name__ == '__main__':
    MyApp().run()