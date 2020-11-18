# Inicializar VM

```
vagrant destroy
vagrant up
vagrant ssh

ln -s /vagrant_data prototipo
python3 -m venv .venv
source .venv/bin/activate

cd prototipo
pip install -r requirements.txt

export FLASK_APP=projeto.app
export FLASK_ENV=development

make initdb

flask shell
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

source .venv/bin/activate
cd prototipo
export FLASK_APP=projeto.app
export FLASK_ENV=development
make run

Ctrl+C
exit
vagrant halt
```

# Browser

```
localhost:5000
```
