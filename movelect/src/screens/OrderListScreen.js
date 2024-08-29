import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, ActivityIndicator, StyleSheet } from 'react-native';
import createAxiosInstance from '../authConfig'; // Asegúrate de que la ruta sea correcta

const OrdersScreen = () => {
  const [pedidos, setPedidos] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPedidos = async () => {
      try {
        const axiosInstance = await createAxiosInstance();
        console.log("axiosInstance: ",axiosInstance);
        const response = await axiosInstance.get('/pedidos/');
        console.log("response: ",response);
        setPedidos(response.data.pedidos);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    fetchPedidos();
  }, []);

  const renderItem = ({ item }) => (
    <View style={styles.row}>
      <Text style={styles.cell}>{item.id}</Text>
      <Text style={styles.cell}>{item.fecha}</Text>
      <Text style={styles.cell}>{item.precio_cuota}</Text>
      <Text style={styles.cell}>{item.estado}</Text>
    </View>
  );

  if (loading) {
    return <ActivityIndicator size="large" color="#0000ff" />;
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerText}>ID Pedido</Text>
        <Text style={styles.headerText}>Fecha</Text>
        <Text style={styles.headerText}>Precio por Cuota</Text>
        <Text style={styles.headerText}>Estado</Text>
      </View>
      <FlatList
        data={pedidos}
        keyExtractor={(item) => item.id ? item.id.toString() : 'key'}
        renderItem={renderItem}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: 'white',
  },
  header: {
    flexDirection: 'row',
    backgroundColor: '#EC7063',
    paddingVertical: 8,
    paddingHorizontal: 16,
    marginBottom: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#ccc',
  },
  headerText: {
    flex: 1,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  row: {
    flexDirection: 'row',
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#ccc',
  },
  cell: {
    flex: 1,
    textAlign: 'center',
  },
});

export default OrdersScreen;
