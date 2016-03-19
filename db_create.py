from app import db, models
db.create_all()

rootAdmin = models.Admin(name="ADMIN", role=models.ROLE_FULL_ADMIN)
rootAdmin.set_password("password")
db.session.add(rootAdmin)
db.session.commit()