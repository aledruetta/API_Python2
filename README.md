# Flask REST API

# Inicializar VM

```
vagrant destroy
vagrant up
vagrant ssh

ln -s /vagrant_data prototipo

  cd prototipo
  make install

  source ~/.venv/bin/activate

  make initdb

  make shell
  import sensor_sim
  sensor_sim.create_all()
  exit

make run
```

# Usar VM

```
vagrant status
vagrant up
vagrant ssh

source ~/.venv/bin/activate
cd prototipo
make run

Ctrl+C
exit
vagrant halt
```

# Browser

```
localhost:5000
```
