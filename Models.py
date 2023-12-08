from DB import main_db, serializer

# Ana veritabanı modeli: Yıkama Makinesi (main_db.sqlite)
class WashingMachine(main_db.Model):
    # Yıkama makinesi için model sınıfı, ana veritabanında bulunan 'washing_machines' tablosunu temsil eder.
    # Modelin özellikleri, veritabanındaki sütunlarla eşleşir.
    id = main_db.Column(main_db.Integer, primary_key=True)        # Makine kimliği
    tag = main_db.Column(main_db.String(50), unique=True)         # Etiket (benzersiz)
    assembly1 = main_db.Column(main_db.DateTime)                  # Montaj tarihleri
    assembly2 = main_db.Column(main_db.DateTime)
    assembly3 = main_db.Column(main_db.DateTime)
    assembly4 = main_db.Column(main_db.DateTime)
    assembly5 = main_db.Column(main_db.DateTime)
    status = main_db.Column(main_db.String(20))                   # Durum (çalışıyor, arızalı vb.)

# Arızalı Makine modeli, farklı veritabanına bağlı (main_db_arizali.sqlite)
class ArizaliMachine(main_db.Model):
    # Arızalı makine modeli, 'arizali' adlı farklı bir veritabanında bulunan 'arizali_database' tablosunu temsil eder.
    # Modelin özellikleri, veritabanındaki sütunlarla eşleşir.
    __bind_key__ = 'arizali'                                      # Farklı veritabanına bağlama
    id = main_db.Column(main_db.Integer, primary_key=True)         # Makine kimliği
    tag = main_db.Column(main_db.String(50), unique=True)          # Etiket (benzersiz)
    assembly1 = main_db.Column(main_db.DateTime)                   # Montaj tarihleri
    assembly2 = main_db.Column(main_db.DateTime)
    assembly3 = main_db.Column(main_db.DateTime)
    assembly4 = main_db.Column(main_db.DateTime)
    assembly5 = main_db.Column(main_db.DateTime)
    Ariza = main_db.Column(main_db.String(20))                     # Arıza açıklaması

# Ürün Şeması
class ProductSchema(serializer.Schema):
    # Ürün şeması, veritabanından çekilen verilerin nasıl serileştirileceğini belirtir.
    class Meta:
        fields = ('id', 'tag', 'assembly1', 'assembly2', 'assembly3', 'assembly4', 'assembly5', 'status')

# Ürün şema nesneleri
machines_schema = ProductSchema(many=True)        # Birden fazla ürünün listesini serileştirmek için kullanılır
machine_schema = ProductSchema()                  # Tek bir ürünün detaylarını serileştirmek için kullanılır
