# Download and unzip data from DWD`s open data server.
wget -q -r --level=1 https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/precipitation/historical/ -P /home/lena/Documents/Master/Sem_2/FachvorträgeHydro/orographic_precipitation/metdata
cd /home/lena/Documents/Master/Sem_2/FachvorträgeHydro/orographic_precipitation/metdata/opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/precipitation/historical
unzip \*.zip