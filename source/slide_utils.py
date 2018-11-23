from IPython.core.display import Image, display, clear_output
import ipywidgets as widgets

class SlideController:
    def __init__(self, base_img_fmt, num_images):
        self.start = 0
        self.end = num_images-1
        self.i = self.start
        
        self.imgs = [ base_img_fmt%i for i in range(num_images) ]
        
        # Add widgets
        btnNext = widgets.Button(description="Next Slide   〉")
        btnPrev = widgets.Button(description="〈   Previous Slide")
        display(widgets.HBox((btnPrev,btnNext)))
        
        self.img_output = widgets.Output()
        display(self.img_output)
        
        # Connect widget events
        btnNext.on_click(lambda ev: self.load( 1))
        btnPrev.on_click(lambda ev: self.load(-1))
        
        # initialize first image
        self.load()

    def step_and_validate(self, step):
        self.i += step
        
        self.i = self.start if self.i<self.start else self.i
        self.i = self.end if self.i>self.end else self.i
        
    def load(self, step=0):
        """Load and Display Image"""
        
        # take a step, if requested
        self.step_and_validate(step)
        
        with self.img_output:
            clear_output(wait=True)
            display(Image(self.imgs[self.i], width=850, unconfined=True))