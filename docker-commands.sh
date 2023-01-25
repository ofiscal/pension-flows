docker run --name pension -itd   \
  -v /home/jeff/of/pensions:/mnt \
  ofiscal/tax.co:latest

docker start pension
docker exec -it pension bash
cd mnt/

docker stop pension && docker rm pension
