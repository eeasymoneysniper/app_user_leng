from APP.basededatos import engine, Base
import APP.modelos as modelos

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    print('Tablas creadas')
