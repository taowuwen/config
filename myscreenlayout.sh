#!/bin/sh
#xrandr --output HDMI-2 --mode 3440x1440_60.00 --pos 1920x0 --rotate normal --output HDMI-1 --off --output DP-1 --off --output eDP-1 --primary --mode 1920x1080 --pos 0x0 --rotate normal --output DP-2 --off

# # 3440x1440 29.95 Hz (CVT) hsync: 43.96 kHz; pclk: 196.25 MHz
# Modeline "3440x1440_30.00"  196.25  3440 3600 3952 4464  1440 1443 1453 1468 -hsync +vsync
# cvt 3440x1440 30


# for x230 hdmi output
#xrandr --newmode "3440x1440_30.00"  196.25  3440 3600 3952 4464  1440 1443 1453 1468 -hsync +vsync
#xrandr --addmode HDMI-2 3440x1440_30.00
#xrandr --output HDMI-2 --mode 3440x1440_30.00 --pos 1920x0 --rotate normal --output HDMI-1 --off --output DP-1 --off --output eDP-1 --primary --mode 1920x1080 --pos 0x0 --rotate normal --output DP-2 --off



xrandr --newmode "3440x1440_100.00"  728.00  3440 3728 4104 4768  1440 1443 1453 1527 -hsync +vsync
xrandr --addmode DP-1 "3440x1440_100.00" 
xrandr --output DP-1 --mode "3440x1440_100.00" --pos 1920x0 --rotate normal --output HDMI-1 --off --output DP-1 --off --output eDP-1 --primary --mode 1920x1080 --pos 0x0 --rotate normal --output DP-2 --off

#xrandr --newmode "3440x1440_30.00"  196.25  3440 3600 3952 4464  1440 1443 1453 1468 -hsync +vsync
#xrandr --addmode HDMI-2 3440x1440_30.00
#xrandr --output HDMI-2 --mode 3440x1440_30.00 --pos 1920x0 --rotate normal --output HDMI-1 --off --output DP-1 --off --output eDP-1 --primary --mode 1920x1080 --pos 0x0 --rotate normal --output DP-2 --off
