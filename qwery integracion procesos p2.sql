create database empleadosGeoreferencia




select * from base_usuarios bu 


insert into base_usuarios (id,Nombre,Apellido,Usuario,Ciudad) values ('2','Pepe','Test','ptest','Ambato')
insert into base_usuarios (id,Nombre,Apellido,Usuario,Ciudad) values ('3','Angela','Castor','acastor','Ambato');
insert into base_usuarios (id,Nombre,Apellido,Usuario,Ciudad) values ('4','Auistin','Tixe','atixe','Machachi');
insert into base_usuarios (id,Nombre,Apellido,Usuario,Ciudad) values ('5','Carlos','Cacierra','ccacierra','Guayaquil');





CREATE TABLE ciudades (
    nombre_ciudad VARCHAR(50),
    georeferenciacion JSON,
    PRIMARY KEY (nombre_ciudad)
);


select * from ciudades