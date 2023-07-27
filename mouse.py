import pyautogui


current_x, current_y = pyautogui.position()
print(f'Current cursor coordinates: X={current_x}, Y={current_y}')

new_x, new_y = 500, 500
pyautogui.moveTo(new_x, new_y)
print(f'Moved cursor to coordinates: X={new_x}, Y={new_y}')

offset_x, offset_y = 100, -50
pyautogui.move(offset_x, offset_y)
print('Moved the cursor 100 pixels to the right and 50 pixels up')


pyautogui.click(x=new_x, y=new_y, button='left')
print('Clicked')






