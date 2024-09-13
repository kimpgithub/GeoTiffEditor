import rasterio
from rasterio.transform import from_origin
from rasterio.crs import CRS
import geopandas as gpd
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

# SHAPE_RESTORE_SHX 옵션 활성화 (shapefile 복구용)
os.environ['SHAPE_RESTORE_SHX'] = 'YES'

# Tkinter로 파일 선택 GUI 구현
def get_file_path(prompt, file_type):
    root = Tk()
    root.withdraw()  # Tkinter 창 숨기기
    file_path = askopenfilename(title=prompt, filetypes=[(file_type, "*.*")])
    return file_path

def save_file_path(prompt):
    root = Tk()
    root.withdraw()  # Tkinter 창 숨기기
    file_path = asksaveasfilename(title=prompt, defaultextension=".tif", filetypes=[("TIF files", "*.tif")])
    return file_path

# Shapefile, TIF 파일 경로 및 출력 경로 선택
shapefile_path = get_file_path("Shapefile 경로를 선택하세요", "Shapefile")
tif_path = get_file_path("TIF 파일 경로를 선택하세요", "TIF")

# 결과 파일 이름 자동 생성 (원본 파일명 뒤에 "_processed" 추가)
output_path = os.path.splitext(tif_path)[0] + "_processed.tif"

# Shapefile 읽기
gdf = gpd.read_file(shapefile_path)

# Shapefile의 경계 범위 추출 (좌상단 x, y 및 우하단 x, y)
bounds = gdf.total_bounds  # 좌상단 x, 좌상단 y, 우하단 x, 우하단 y
top_left_easting, bottom_right_northing, bottom_right_easting, top_left_northing = bounds

# 좌표 범위에 50m 옵셋 적용
top_left_easting -= 50  # 좌측 x 좌표에 50m 옵셋 적용
top_left_northing += 50  # 상단 y 좌표에 50m 옵셋 적용
bottom_right_easting += 50  # 우측 x 좌표에 50m 옵셋 적용
bottom_right_northing -= 50  # 하단 y 좌표에 50m 옵셋 적용

# TIF 파일 읽기
with rasterio.open(tif_path) as src:
    # 이미지 데이터 및 프로필 불러오기
    image_data = src.read()
    profile = src.profile

    # 이미지 크기 확인 (픽셀 단위로 폭과 높이 가져오기)
    width = src.width
    height = src.height

    # 픽셀 크기 계산 (좌표 범위 / 이미지 크기)
    pixel_size_x = (bottom_right_easting - top_left_easting) / width
    pixel_size_y = (top_left_northing - bottom_right_northing) / height

    # 변환 설정 (왼쪽 상단 좌표와 계산된 픽셀 크기)
    transform = from_origin(top_left_easting, top_left_northing, pixel_size_x, pixel_size_y)

    # 프로필 업데이트 (좌표계 및 변환 적용)
    profile.update({
        'crs': CRS.from_epsg(5186),  # 명확하게 EPSG 코드를 사용하여 좌표계 설정
        'transform': transform,  # 변환 설정
        'driver': 'GTiff',
        'count': src.count,  # 밴드 수 유지
    })

    # 새로운 TIF 파일에 메타데이터 포함하여 저장
    with rasterio.open(output_path, 'w', **profile) as dst:
        dst.write(image_data)

print(f"TIF 파일에 Shapefile 기반 좌표 범위 적용 후 저장 완료: {output_path}")
