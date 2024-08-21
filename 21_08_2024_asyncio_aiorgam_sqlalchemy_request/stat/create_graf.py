import matplotlib.pyplot as plt
import io
from PIL import Image
import time
import asyncio
from repository import Repo


check_list = ["USD", "EURO", "RUB", "CNY"]
Day = []
Cur = []
insert_type = input("аббревиатура: ")
if insert_type not in check_list:
	print('увы :(')


async def select_current(insert_type):
    result = await Repo.select_current(insert_type)
    for row in result:
	    str_mont = str(row.date)
	    Day.append(str_mont[8:])
	    str_buy = str(row.actual_current)
	    int_buy = float(str_buy)
	    Cur.append(int_buy)

asyncio.run(select_current(insert_type))

print("Share_buy", Cur)
print("Month", Day)

# Plotting Line Graph
plt.title("Стат за 7 дней")
plt.xlabel('День')
plt.ylabel("Курс")
plt.plot(Day, Cur)

# Getting the current figure and save it in the variable.
figure = plt.gcf()

# Create a Function for Converting a figure to a PIL Image.

def fig2img(fig):
	buf = io.BytesIO()
	fig.savefig(buf)
	buf.seek(0)
	img = Image.open(buf)
	return img


# Save return image in a variable by passing
# plot in the created function for Converting a plot to a PIL Image.
img = fig2img(figure)
#current_date = time_str = time.strftime("%Y-%m-%d %H:%M:%S")
# Save image with the help of save() Function.
img.save(f'image/image_{insert_type}.png')
