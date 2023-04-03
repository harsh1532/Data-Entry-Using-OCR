<h1 align="center">Data Entry using OCR</h1>

Data Entry Using Optical Character Recognition (OCR) is a system that scans a sheet of data, which includes numbers and characters, and saves it into .csv files.


## Description

The main idea of this system is to save the efforts and time of human beings as they would not require to perform data entry operations manually.The onerous work of text localization and detection is easily and accurately handled by Tesseract software, which takes the image, and generates an output in form of text.

## Tools used

- [Python](https://www.python.org/)
- [Anaconda](https://www.anaconda.com/products/individual)
- [VS Code](https://code.visualstudio.com/download)
- [Tesseract Engine](https://github.com/tesseract-ocr/tesseract) (Watch on Youtube how to download the Tesseract s/w)

## Libraries involved

* __Python (3.8.5)__
* __NumPy (1.20.1)__
* __PIL (8.1.0)__
* __OpenCV (4.0.1)__
* __Pytesseract (0.3.4)__
* __Tkinter (8.6)__
* __imutils (0.5.4)__
* __Pickle (4.0)__
* __ttkthemes (2.3.0)__

## Steps to Follow

- Choose particular type of form you want to scan.
- Select the template image and save it using the **New Form** menu.
- Now, you can scan and extract text from **millions** of that particular type of filled-form images using **Old Form** menu.
<br></br>
<h2 align="center"> NEW FORM </h2>

### 1) Open New Form
<p align="center">
  <img src="https://github.com/patelharshsupport/GIF-for-readme/blob/main/Open%20New%20Form%20ver1.gif?raw=true">
</p>

Select **New Form** from the menu bar and browse the image of the template you want to scan.
Please try to use **digital copy** of the template so that scanned paper forms can be easily aligned according to the template image which can result in better accuracy.
<br></br>
### 2) Naming and Creating ROI
<p align="center">
  <img src="https://github.com/patelharshsupport/GIF-for-readme/blob/main/Naming%20and%20Creating%20ROI%20ver1.gif?raw=true">
</p>

Firstly, Enter the name of the form and start selecting the region of interest (ROI) where you want to detect the text. Then, Enter the name of the attribute in the pop-up and press **OK**. After selecting all the attributes, press **Save** button to save the form details. (Now, you can move to old form window.)
<br></br>
### 3) ROI Mistake
<p align="center">
  <img src="https://github.com/patelharshsupport/GIF-for-readme/blob/main/ROI%20Mistake%20ver1.gif?raw=true">
</p>

When you make a mistake while drawing Region of Interest (ROI). You can use **Cancel** button to undo your action.
<br></br>
<br></br>
<h2 align="center">OLD FORM</h2>

### 1) Open and Browse Old Form

<p align="center">
  <img src="https://github.com/patelharshsupport/GIF-for-readme/blob/main/Open%20and%20Browse%20Old%20Form%20ver1.gif?raw=true">
</p>

Select **Old Form** from the menu bar. Select the form you want to work on from the dropdown list and browse the filled-form image.
<br></br>
### 2) Scan, Edit and Save

<p align="center">
  <img src="https://github.com/patelharshsupport/GIF-for-readme/blob/main/Scan,%20Edit%20and%20Save%20ver1.gif?raw=true">
</p>

Press **Scan** button to scan the contents of the selected image. Check the results and **correct** if detected wrong. (As machines make mistakes too. They don't have mind but you have one :rofl:). Finally, press the **Save** button to save the result to .csv file.


