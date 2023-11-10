import os
os.environ['DEVELOPMENT'] = 'DEVELOPMENT'
# See https://github.com/aquacropos/aquacrop/tree/master
from aquacrop import AquaCropModel, Soil, Crop, InitialWaterContent
from aquacrop.utils import prepare_weather, get_filepath
import pandas as pd
weather_file_path = get_filepath('tunis_climate.txt')
model_os = AquaCropModel(
            sim_start_time=f"{1979}/10/01",
            sim_end_time=f"{1985}/05/30",
            weather_df=prepare_weather(weather_file_path),
            soil=Soil(soil_type='SandyLoam'),
            crop=Crop('Wheat', planting_date='10/01'),
            initial_water_content=InitialWaterContent(value=['FC']),
        )
model_os.run_model(till_termination=True)
model_results = model_os.get_simulation_results()

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

print(model_results)
