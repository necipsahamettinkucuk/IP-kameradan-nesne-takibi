from flask import jsonify, request
from Models import WashingMachine, ArizaliMachine, machine_schema, machines_schema
from DB import app, main_db
from datetime import datetime
from id_list import id_generator


# Yeni bir referans etiketi alın
def get_next_reference_tag(id_generator):
    return f'Machine_{id_generator}'


# ----------------- POST METHODS -----------------

# Makine ekleme endpoint'i
@app.route('/add_machine', methods=['POST'])
def add_machine():
    try:
        if not id_generator:
            return jsonify(error='Unique id listesi tükenmiş'), 400

        with app.app_context():
            new_id = next(id_generator)  # Bir sonraki unique id'yi al
            new_machine = WashingMachine(
                tag=get_next_reference_tag(new_id),
                assembly1=datetime.now(),
                status='Arizasiz',
                id=new_id
            )

            # Eğer yeni makinenin durumu "Arızalı" ise, yeni makineyi ArizaliMachine modeliyle oluşturur.
            if new_machine.status.lower() == 'arızalı':
                new_machine = ArizaliMachine(
                    tag=new_machine.tag,
                    assembly1=new_machine.assembly1,
                    id=new_machine.id,
                    Ariza='Arızalı'
                )

            main_db.session.add(new_machine)
            main_db.session.commit()
            return jsonify(message='Makine Eklendi')
    except Exception as e:
        main_db.session.rollback()
        return jsonify(error='Hata oluştu', details=str(e)), 500


# Montaj güncelleme endpoint'i
@app.route('/update_assembly', methods=['POST'])
def update_assembly():
    try:
        data = request.json

        if 'assembly_num' not in data or 'id' not in data:
            return jsonify({'error': 'Gerekli veri alanları eksik'}), 400

        assembly_num = data['assembly_num']
        id = data['id']  # Makinenin etiketi

        with app.app_context():
            machine = WashingMachine.query.filter_by(id=id).first()

            if not machine:
                return jsonify({'error': f'{id} etiketli makine bulunamadı'}), 404

            if not (1 <= assembly_num <= 5):  # Montaj numarası 1 ile 5 arasında olmalı
                return jsonify({'error': 'Geçersiz montaj numarası'}), 400

            assembly_column = f'assembly{assembly_num}'
            setattr(machine, assembly_column, datetime.now())

            main_db.session.commit()
            return jsonify({'message': f'{id} makinesinin Assembly{assembly_num} güncellendi'}), 200
    except Exception as e:
        main_db.session.rollback()
        return jsonify(error='Hata oluştu', details=str(e)), 500


# Arizali/Tamir kısmına Makine girince status'u updateliyoruz
@app.route('/update_status', methods=['POST'])
def update_status():
    try:
        data = request.json

        if 'id' not in data:
            return jsonify({'error': 'Gerekli veri alanları eksik'}), 400

        id = data['id']
        machine = WashingMachine.query.get(id)

        if not machine:
            return jsonify({'error': f'{id} ID\'li makine bulunamadı'}), 404

        # Makine durumunu "Arızalı" olarak güncelle
        machine.status = 'Arızalı'
        main_db.session.commit()

        return jsonify({'message': f'{id} ID\'li makinenin durumu "Arızalı" olarak güncellendi'}), 200
    except Exception as e:
        main_db.session.rollback()
        return jsonify(error='Hata oluştu', details=str(e)), 500


# ----------------- GET METHODS -----------------

# Id'si belirli makinenin herhangi bir assembly_Num kısmının True(yani o istasyondan geçmiş) ya da False(yani o istasyondan geçmemiş) olma durumu
@app.route('/assembly_control', methods=['GET'])
def assembly_control():
    try:
        data = request.json

        id = data['id']
        assembly_num = data['assembly_num']
        if 'id' not in data or 'assembly_num' not in data:
            assembly_status = False
            return jsonify({f'assembly{assembly_num}_status': assembly_status})

        machine = WashingMachine.query.get(id)

        if not machine:
            assembly_status = False
            return jsonify({f'assembly{assembly_num}_status': assembly_status})

        else:
            assembly_column = f'assembly{assembly_num}'
            assembly_status = bool(
                getattr(machine, assembly_column))  # Montaj numarasına göre sütun adını kullanarak durumu al
            # Eğer montaj istasyonunda bir tarih yoksa bool(none) --> False dönecek
            # Eğer montaj istasyonunda bir tarih varsa bool("2023-08-31T15:29:34.687007")--> True dönecek
        return jsonify({f'assembly{assembly_num}_status': assembly_status})
    except Exception as e:
        return jsonify(error='Hata oluştu', details=str(e)), 500


# Arızalı makineleri getirme endpoint'i
@app.route('/get_all_arizali', methods=['GET'])
def get_all_arizali():
    try:
        arizali_machines = ArizaliMachine.query.all()
        result = []

        for arizali_machine in arizali_machines:
            ariza_assemblies = []

            if arizali_machine.Ariza:
                assembly_numbers = arizali_machine.Ariza.split(', ')
                for assembly_number in assembly_numbers:
                    if assembly_number.startswith('Assembly'):
                        ariza_assemblies.append(assembly_number)

            result.append({
                "assembly1": arizali_machine.assembly1,
                "assembly2": arizali_machine.assembly2,
                "assembly3": arizali_machine.assembly3,
                "assembly4": arizali_machine.assembly4,
                "assembly5": arizali_machine.assembly5,
                "id": arizali_machine.id,
                "tag": arizali_machine.tag,
                "Ariza": ', '.join(ariza_assemblies)
            })

        return jsonify(result)
    except Exception as e:
        return jsonify(error='Hata oluştu', details=str(e)), 500


# Tüm makineleri getirme endpoint'i
@app.route('/get_all_machines', methods=['GET'])
def get_all_machines():
    try:
        all_machines = WashingMachine.query.all()
        result = machines_schema.dump(all_machines)
        return jsonify(result)
    except Exception as e:
        return jsonify(error='Hata oluştu', details=str(e)), 500


# Belirli bir makineyi getirme endpoint'i
@app.route('/get_single_machine/<int:id>', methods=['GET'])
def get_single_machine(id):
    try:
        product = WashingMachine.query.get(id)
        return machine_schema.jsonify(product)
    except Exception as e:
        return jsonify(error='Hata oluştu', details=str(e)), 500


# ----------------- Main -----------------


# Uygulama çalıştırma ve veritabanını oluşturma
if __name__ == '__main__':
    with app.app_context():
        main_db.create_all()  # Veritabanını oluştur
    app.run('', debug=True)  # Uygulamayı çalıştır ve hata ayıklama modunu aç