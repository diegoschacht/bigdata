Pasos para correr el programa 

1. Instalar Apache Flink
2. Configurar las dependencias
 <dependencies>
    <dependency>
        <groupId>com.google.cloud</groupId>
        <artifactId>google-cloud-language</artifactId>
        <version>1.74.0</version>
    </dependency>
        <dependency>
            <groupId>org.apache.flink</groupId>
            <artifactId>flink-java</artifactId>
            <version>1.8.0</version>
        </dependency>
        <dependency>
            <groupId>org.apache.flink</groupId>
            <artifactId>flink-clients_2.12</artifactId>
            <version>1.8.0</version>
        </dependency>
    </dependencies>
3. Configurar la variable de entorno para obtener la Key de Google Credencials
4. Correr el sistema!