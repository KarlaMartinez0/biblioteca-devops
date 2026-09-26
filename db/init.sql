CREATE TABLE IF NOT EXISTS libros (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    autor VARCHAR(100) NOT NULL,
    genero VARCHAR(50),
    anio INT,
    copias INT DEFAULT 1
);

INSERT INTO libros (titulo, autor, genero, anio, copias)
VALUES
    ('Cien años de soledad', 'Gabriel García Márquez', 'Novela', 1967, 3),
    ('1984', 'George Orwell', 'Ciencia ficción', 1949, 2);