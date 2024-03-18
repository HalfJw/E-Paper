#!/usr/bin/python
# -*- coding:utf-8 -*-

import calendar
import locale
import logging
import os
import random
import sys
import time
from datetime import datetime

import schedule
from PIL import Image, ImageDraw, ImageFont, ImageOps
from PIL.Image import Image as TImage
from PIL.ImageDraw import ImageDraw as TImageDraw

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
    
import logging
from waveshare_epd import epd7in5b_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd7in5b_V2 Demo")

    epd = epd7in5b_V2.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    
    DEBUG = False
    
    FONT_ROBOTO_DATE = ImageFont.truetype(
    os.path.join(FONT_DICT, 'Roboto-Black.ttf'), 200)
    FONT_ROBOTO_H1 = ImageFont.truetype(
    os.path.join(FONT_DICT, 'Roboto-Black.ttf'), 40)
    FONT_ROBOTO_H2 = ImageFont.truetype(
    os.path.join(FONT_DICT, 'Roboto-Black.ttf'), 30)
    FONT_ROBOTO_P = ImageFont.truetype(
    os.path.join(FONT_DICT, 'Roboto-Black.ttf'), 20)
    FONT_POPPINS_BOLT_P = ImageFont.truetype(
    os.path.join(FONT_DICT, 'Poppins-Bold.ttf'), 22)
    FONT_POPPINS_P = ImageFont.truetype(
    os.path.join(FONT_DICT, 'Poppins-Regular.ttf'), 20)
    LINE_WIDTH = 3
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    
    current_time = datetime.datetime.now()
    
    hour = current_time.hour
    minute = current_time.min
    
    # Drawing on the Horizontal image
    if DEBUG:
            logger.info("DEBUG-Mode activated...")

            image_blk = Image.open(os.path.join(
            PICTURE_DICT, "blank-aperture.bmp"))
            image_red = Image.open(os.path.join(
            PICTURE_DICT, "blank-hk.bmp"))

            draw_blk = ImageDraw.Draw(image_blk)
            draw_red = ImageDraw.Draw(image_red)

            render_content(draw_blk, image_blk, draw_red,
                       image_red, epd.width, epd.height)
            show_content(epd, image_blk, image_red)
        # clear_content(epd)
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5b_V2.epdconfig.module_exit(cleanup=True)
    exit()
    
    
    
    
def render_content(draw_blk: TImageDraw, image_blk: TImage,  draw_red: TImageDraw, image_red: TImage, height: int, width: int):
    locale.setlocale(locale.LC_ALL, LOCALE)

    PADDING_L = int(width/10)
    PADDING_TOP = int(height/100)
    now = time.localtime()
    max_days_in_month = calendar.monthrange(now.tm_year, now.tm_mon)[1]
    day_str = time.strftime("%A")
    day_number = now.tm_mday
    month_str = time.strftime("%B")

    # draw_text_centered(str(day_number), (width/2, 0), draw_blk, FONT_ROBOTO_H1)

    # Heading
    current_height = height/20
    draw_blk.line((PADDING_L, current_height, width, current_height),
                  fill=1, width=LINE_WIDTH)
    draw_blk.text((PADDING_L, current_height), month_str.upper(),
                  font=FONT_ROBOTO_H2, fill=1)
    current_height += get_font_height(FONT_ROBOTO_H2)

    # Date
    current_font_height = get_font_height(FONT_ROBOTO_DATE)
    draw_blk.text((PADDING_L, current_height - current_font_height/10),
                  str(day_number), font=FONT_ROBOTO_DATE, fill=1)
    current_height += current_font_height

    # Month-Overview (with day-string)
    current_height += PADDING_TOP
    day_of_month = str(day_number) + "/" + str(max_days_in_month)
    draw_blk.text((PADDING_L, current_height), day_of_month,
                  font=FONT_ROBOTO_P, fill=1)

    tmp_right_aligned = width - \
        get_font_width(FONT_ROBOTO_P, day_str.upper()) - PADDING_L/4
    draw_blk.text((tmp_right_aligned, current_height), day_str.upper(),
                  font=FONT_ROBOTO_P, fill=1)

    current_height += get_font_height(FONT_ROBOTO_P) + PADDING_TOP
    draw_blk.line((PADDING_L, current_height, width, current_height),
                  fill=1, width=LINE_WIDTH)

    # Month-Tally-Overview
    current_height += PADDING_TOP
    tally_height = height/40
    tally_width = LINE_WIDTH + width/120  # width + padding
    available_width = width - PADDING_L
    tally_number = int(available_width / tally_width *
                       (day_number / max_days_in_month))
    x_position = PADDING_L + LINE_WIDTH/2
    for i in range(0, tally_number):
        draw_blk.line((x_position, current_height, x_position,
                      current_height + tally_height), fill=1, width=LINE_WIDTH)
        x_position += tally_width
    current_height += tally_height

    # Calendar
    current_height += height/40
    event_list = get_events(6)

    last_event_day = datetime.now().date()
    for event in event_list:
        # Draw new day
        if last_event_day != event.start.date():
            # current_height += height/40
            last_event_day = event.start.date()
            # day_string = "{} {}".format(last_event_day.day,
            #                               last_event_day.strftime("%a"))
            day_string = last_event_day.strftime("%a %d")
            draw_blk.text((PADDING_L, current_height), day_string,
                          font=FONT_ROBOTO_P, fill=1)
            current_height += get_font_height(FONT_ROBOTO_P)
        
def show_content(epd: eInk.EPD, image_blk: TImage, image_red: TImage):
    logger.info("Exporting finial images")
    image_blk.save("EXPORT-black.bmp")
    image_red.save("EXPORT-red.bmp")
    if ROTATE_IMAGE:
        image_blk = image_blk.rotate(180)
        image_red = image_red.rotate(180)
    if not DEBUG:
        init_display(epd)
        logger.info("Writing on display")
        epd.display(epd.getbuffer(image_blk), epd.getbuffer(image_red))
        set_sleep(epd)


def clear_content(epd: eInk.EPD):
    if DEBUG:
        logger.warning("Clear has no effect while debugging")
    else:
        init_display(epd)
        clear_display(epd)
        set_sleep(epd)
