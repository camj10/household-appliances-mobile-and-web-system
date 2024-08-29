// ProductDetailsScreen.js
import React, { useEffect, useState } from 'react';
import { View, Text, Image, StyleSheet, ActivityIndicator, Button } from 'react-native';
import createAxiosInstance from '../authConfig'; // Verifica la ruta correcta

const BASE_URL = 'http://localhost:8000/media/imagenes/'; // URL base para las imágenes

const ProductDetailsScreen = ({ route, navigation }) => {
  const { productId } = route.params;
  const [product, setProduct] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProductDetails = async () => {
      try {
        const axiosInstance = await createAxiosInstance();
        const response = await axiosInstance.get(`/detalleproducto/${productId}/`);
        console.log("response.data: ", response.data);
        setProduct(response.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching product details:', error.response ? error.response.data : error.message);
        setError('Error fetching product details');
        setLoading(false);
      }
    };

    fetchProductDetails();
  }, [productId]);

  if (error) {
    return <View style={styles.container}><Text>{error}</Text></View>;
  }

  if (loading) {
    return <View style={styles.container}><ActivityIndicator size="large" color="#0000ff" /></View>;
  }

  return (
    <View style={styles.outerContainer}>
      <View style={styles.innerContainer}>
        {product.imagen && (
          <Image
            source={{ uri: `${BASE_URL}${product.imagen}` }}
            style={styles.image}
            resizeMode='contain'
          />
        )}
        <Text style={styles.title}>{product.descripcion}</Text>
        <Text>Marca: {product.marca}</Text>
        <Text>Precio Total: {product.precio_total}</Text>
        <Text>Stock: {product.stock}</Text>
        <Text>Cantidad de Cuotas: {product.cantidad_cuotas}</Text>
        <Text>Precio por Cuota: {product.precio_cuota}</Text>
        <Button title="Volver" onPress={() => navigation.goBack()} />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  outerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#f8f8f8', // Cambia el color de fondo según sea necesario
  },
  innerContainer: {
    width: '90%', // Puedes ajustar esto según sea necesario
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.8,
    shadowRadius: 2,
    elevation: 5,
  },
  image: {
    width: '100%',
    height: 200,
    marginBottom: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginVertical: 10,
    textAlign: 'center',
  },
});

export default ProductDetailsScreen;
