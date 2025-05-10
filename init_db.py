from app import create_app, db
from app.services.db_init import init_db
from sqlalchemy import inspect, text

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # 創建所有表格
        db.create_all()

        # 檢查 users 表格是否存在 auto_login_token 欄位
        inspector = inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('users')]

        # 如果欄位不存在，則添加該欄位
        if 'auto_login_token' not in columns:
            try:
                print('Adding auto_login_token column to users table...')
                with db.engine.connect() as conn:
                    conn.execute(text('ALTER TABLE users ADD COLUMN auto_login_token VARCHAR(255)'))
                    conn.execute(text('CREATE INDEX ix_users_auto_login_token ON users (auto_login_token)'))
                    conn.commit()
                print('auto_login_token column added successfully.')
            except Exception as e:
                print(f'Error adding auto_login_token column: {e}')

        # 檢查 auto_login_pin 欄位
        if 'auto_login_pin' not in columns:
            try:
                print('Adding auto_login_pin column to users table...')
                with db.engine.connect() as conn:
                    conn.execute(text('ALTER TABLE users ADD COLUMN auto_login_pin VARCHAR(6)'))
                    conn.commit()
                print('auto_login_pin column added successfully.')
            except Exception as e:
                print(f'Error adding auto_login_pin column: {e}')

        # 初始化數據
        init_db()
        print('Database initialized successfully!')