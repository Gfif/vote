for i in {1..5}
do
  openssl genrsa -out s$i 4096
  openssl rsa -in s$i -pubout > s$i.pub
done
for i in {1..5}
do 
  openssl genrsa -out c$i 1024
  openssl rsa -in c$i -pubout > c$i.pub
done

