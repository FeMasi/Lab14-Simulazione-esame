from database.DB_connect import DBConnect
from model.gene import Gene

class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllChromosome():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """SELECT DISTINCT Chromosome 
                    FROM GENES
                    WHERE Chromosome > 0"""
        cursor.execute(query)
        for row in cursor:
            result.append(row['Chromosome'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllGenes():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """SELECT * 
                        FROM GENES"""
        cursor.execute(query)
        for row in cursor:
            result.append(Gene(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllConnectedGenes():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """SELECT g1.GeneID as Gene1, g2.GeneID as Gene2, i.Expression_Corr as Expression_Corr
                    FROM genes g1, genes g2, interactions i
                    WHERE g1.GeneID = i.GeneID1 AND g2.GeneID = i.GeneID2
                    AND g1.Chromosome != g2.Chromosome
                    AND g1.Chromosome > 0
                    AND g2.Chromosome > 0
                    GROUP BY g1.GeneID, g2.geneID"""

        cursor.execute(query)

        for row in cursor:
            result.append((row['Gene1'], row['Gene2'], row['Expression_Corr']))

        cursor.close()
        conn.close()
        return result