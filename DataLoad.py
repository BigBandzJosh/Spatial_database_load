import pyproj
import fiona
import shapely
import shapely.geometry
from shapely.ops import transform
import psycopg

db_name = 'Transit'
db_user = 'postgres'
db_password = 'Cruha7aj!'

def connect_db():
  try:
    conn = psycopg.connect(dbname=db_name, user=db_user, password=db_password)
    print(f'Success! Connected to the DB. {db_name}')
    return conn
  except psycopg.Error as e:
    print(f'Error connecting to the database: {e}')
    return None
  
def transform_geomtry():
  with fiona.open('transit.gpkg', mode='r') as gpkg:
    
    source_crs = pyproj.CRS.from_wkt(gpkg.crs_wkt)
    target_crs = pyproj.CRS.from_epsg(2961)
    conversion = pyproj.Transformer.from_crs(source_crs, target_crs, always_xy=True).transform

    with fiona.open('transit_transformed.gpkg', 'w', driver='GPKG', crs=target_crs, schema=gpkg.schema) as output:

      features = []
      for feature in gpkg:
        geom = shapely.geometry.shape(feature['geometry'])
        geom = transform(conversion, geom)
        geom = shapely.geometry.mapping(geom)

        feature = {
          'geometry': geom,
          'properties': feature['properties']
        }
        features.append(feature)
      output.writerecords(features)
      
       
def test_read_gpkg(file_path):
    
    try:
        # Open the GeoPackage file
        with fiona.open(file_path, 'r') as source:
            print(f"Number of features: {len(source)}")
            print(f"CRS: {source.crs}")
            print(f"Driver: {source.driver}")
            print("Layer schema:")
            print(source.schema)
            
            # Print the first feature
            first_feature = next(iter(source), None)
            print("First feature:")
            print(first_feature)
    except Exception as e:
        print(f"An error occurred: {e}")

    
def update_table():
 

if __name__ == '__main__':
  conn = connect_db()
  file = 'transit_transformed.gpkg'
  test_read_gpkg(file)

  # transform_geomtry()
update_table()
  

    
