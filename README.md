# GeoTiffEditor
Shapefile에서 좌표 정보를 추출해 TIF 이미지에 적용하고, 파일 저장 경로를 사용자로부터 입력받아 새로운 TIF 파일로 저장하는 코드입니다.

1. 환경 구성 (window 64bit, conda env)

   conda create -n {가상환경이름} python=3.8
   git clone https://github.com/kimpgithub/GeoTiffEditor.git
   cd GeoTiffEditor
   conda install -c conda-forge geopandas rasterio proj gdal

2. 국토지리정보원 데이터 다운로드
   https://map.ngii.go.kr/ms/map/NlipMap.do

![image](https://github.com/user-attachments/assets/7114328a-6da5-4d30-8214-cb6141128f0a)
  정사영상 다운로드 및 위치 기억

![image](https://github.com/user-attachments/assets/cd02b3c6-f5e9-4755-ac46-97315ada8f6f)
  같은 위치의 수치지형도 다운로드

3. 코드 실행

  cli 명령어 : python main.py
  1) shp 파일 선택
     ![image](https://github.com/user-attachments/assets/664e14a5-3fd3-489b-931d-7b29756a720e)

  2) tif 파일 선택
     ![image](https://github.com/user-attachments/assets/02653e98-4b6d-4e79-b177-8c72bb0884a7)

  3) input_tif_processed.tif 결과 생성
     ![image](https://github.com/user-attachments/assets/57a07fb1-65bb-497a-96cf-da15ef28bd0f)
