import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, ActivityIndicator, StyleSheet } from 'react-native';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const AccountStatusScreen = () => {
  const [cuotas, setCuotas] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCuotas = async () => {
      const token = await AsyncStorage.getItem('access_token');
      try {
        const response = await axios.get('http://localhost:8000/estadocuenta/', {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
        setCuotas(response.data.cuotas);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    fetchCuotas();
  }, []);

  const renderItem = ({ item }) => (
    <View style={styles.row}>
      <Text style={styles.cell}>{item.numero_cuota}</Text>
      <Text style={styles.cell}>{item.precio_cuota}</Text>
      <Text style={styles.cell}>{item.fecha_vencimiento}</Text>
      <Text style={styles.cell}>{item.estado_pago === '0' ? 'No Pagado' : 'Pagado'}</Text>
    </View>
  );

  if (loading) {
    return <ActivityIndicator size="large" color="#0000ff" />;
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerText}>Número de Cuota</Text>
        <Text style={styles.headerText}>Precio de Cuota</Text>
        <Text style={styles.headerText}>Fecha de Vencimiento</Text>
        <Text style={styles.headerText}>Estado de Pago</Text>
      </View>
      <FlatList
        data={cuotas}
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

export default AccountStatusScreen;
