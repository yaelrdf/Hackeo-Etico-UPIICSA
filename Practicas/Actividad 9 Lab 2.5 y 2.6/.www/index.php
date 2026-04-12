<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Formulario de Ingreso</title>
</head>
<body>

<form name="ingresar" action="" method="POST">
    <input type="text" name="correo" value="correo@gmail.com" />
    <br><br>
    <input type="password" name="clave" value="clave" />
    <br><br>
    <input type="submit" name="enviar" value="ingresar" />
</form>

<?php
if (isset($_POST['enviar'])) {
    echo "----------- Backend -----------";
    
    $correo = htmlspecialchars($_POST['correo']);
    $clave  = htmlspecialchars($_POST['clave']);
    
    echo "<br>correo electrónico: $correo";
    echo "<br>clave: $clave";
}
?>

</body>
</html>
