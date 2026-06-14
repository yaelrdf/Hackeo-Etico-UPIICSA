# Peruggia Docker Compose Setup

This docker-compose configuration provides a complete, ready-to-use environment for running Peruggia, a vulnerable web application designed for security training and practice.

## Quick Start

### 1. Start the Services

```bash
docker-compose -f perugiia.yml up -d
```

This will:
- Create and start a MySQL 8.0 database container
- Build and start a PHP 8.2 Apache web server container with necessary PHP extensions
- Set up persistent MySQL data storage

### 2. Initialize Peruggia

1. Open your browser and navigate to: `http://localhost:8080/install.php`
2. Follow the installation wizard
3. Use the default credentials:
   - **Username**: `admin`
   - **Password**: `password`

### 3. Access Peruggia

After installation completes, go to: `http://localhost:8080`

## Configuration

### Database Credentials

The default MySQL credentials are configured in `perugiia.yml`:
- **Root Password**: `root`
- **Database**: `target`
- **User**: `peruggia`
- **Password**: `peruggia123`

### Modify Vulnerabilities

To enable/disable specific vulnerabilities, edit the Peruggia configuration:

1. Access the running container:
   ```bash
   docker exec -it peruggia-web bash
   ```

2. Edit `/var/www/html/conf.php` and modify the vulnerability flags:
   ```php
   $guard_pers_xss = true;      // Persistent XSS blocking
   $guard_refl_xss = true;      // Reflected XSS blocking
   $guard_sqli = true;          // SQL Injection blocking
   $guard_auth_sqli = true;     // Auth bypass SQL Injection blocking
   $guard_lfi = true;           // Local File Inclusion blocking
   $guard_rfi = true;           // Remote File Inclusion blocking
   $guard_fuv = true;           // File Upload Vulnerabilities blocking
   ```

## Useful Commands

### View Logs
```bash
docker-compose -f perugiia.yml logs -f web
docker-compose -f perugiia.yml logs -f mysql
```

### Access the Web Container
```bash
docker exec -it peruggia-web bash
```

### Access MySQL from Container
```bash
docker exec -it peruggia-mysql mysql -u root -p target
```

### Stop Services
```bash
docker-compose -f perugiia.yml down
```

### Remove Everything (Including Data)
```bash
docker-compose -f perugiia.yml down -v
```

## Ports

- **Web Server**: `http://localhost:8080`
- **MySQL**: `localhost:3306`

## Important Notes

⚠️ **Security Warning**: These are REAL vulnerabilities. Only run this in a secure, isolated testing environment.

- The application stores data in a persistent Docker volume (`mysql-data`)
- All services restart automatically unless manually stopped
- The MySQL service includes health checks to ensure the database is ready before the web service starts

## Troubleshooting

### PHP Extensions Not Loading
The Dockerfile automatically installs required PHP extensions (mysqli, pdo_mysql). If issues persist:
```bash
docker-compose -f perugiia.yml down
docker-compose -f perugiia.yml up -d --build
```

### Database Connection Issues
Ensure the MySQL service is running and healthy:
```bash
docker ps
docker-compose -f perugiia.yml ps
```

### Permission Issues
The web server runs as `www-data` user with proper permissions set in the Dockerfile.
