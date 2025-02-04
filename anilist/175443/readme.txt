original image (o-original.jpg) oversaturated by 125% (saturate(1.25) in css filter terms) and zoomed in by 120% (background-size: 1.20)
cuz the colours weren't bright enough imo + characters too far

magick .\o-original.jpg -modulate 100,125 -distort SRT '1.2 0' .\original.jpg