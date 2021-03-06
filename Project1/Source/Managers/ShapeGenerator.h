#pragma once

#define SHAPE_GENERATOR ShapeGenerator::GetInstance()

class Mesh;

/*!
 * Generate Meshes according to a set
 * of preset shapes
 * 
 */
class ShapeGenerator
{
public:
	/*!
	 * Get the ShapeGenerator Singleton reference
	 * 
	 * \return The ShapeGenerator reference
	 */
	GEAR_API static ShapeGenerator* GetInstance();
	/*!
	 * Generate the preset shape Meshes
	 * 
	 */
	GEAR_API void Init();
	/*!
	 * Checks if the given string matches one
	 * of the preset shape Meshes that can be
	 * generated by the ShapeGenerator
	 * 
	 * \param a_type The name of the shape mesh that is being queried
	 * \return A flag that is true if the described shape Mesh can be generated, false otherwise
	 */
	GEAR_API bool IsShape(std::string a_type);
	/*!
	 * Get the Mesh that corresponds to the
	 * given type
	 * 
	 * \param a_type The type of shape that is to be returned
	 * \return The Mesh corresponding to the given type
	 */
	GEAR_API Mesh* GetShapeMesh(std::string a_type);
	/*!
	 * Get a list of all the types of the shapes
	 * that can be generated
	 *
	 * \return A list of all the types of the shapes that can be generated
	 */
	GEAR_API std::vector<std::string> GetShapeTypes();
	/*!
	 * Delete the ShapeGenerator Singleton
	 * 
	 */
	GEAR_API void Cleanup();

private:
	GEAR_API ShapeGenerator();
	GEAR_API ~ShapeGenerator();
	GEAR_API Mesh* GenerateSphere();
	GEAR_API Mesh* GenerateQuad();
	GEAR_API Mesh* GenerateCube();
	GEAR_API Mesh* GenerateCubeInstanced();
	GEAR_API Mesh* GenerateTetrahedron();
	GEAR_API Mesh* GenerateOctahedron();
	GEAR_API Mesh* GenerateIcosahedron();
	GEAR_API Mesh* GenerateCylinder();
	GEAR_API Mesh* GenerateCapsule();
	GEAR_API void GenerateCubeFace(Mesh* a_pMesh, glm::mat4 a_transformation);
	GEAR_API void GenerateIcosahedronFace(Mesh* a_pMesh, glm::vec3 a_vertPos1, glm::vec3 a_vertPos2, glm::vec3 a_vertPos3);
	GEAR_API void SetMinMax(Mesh* a_pMesh);
	GEAR_API void CalculateTangents(Mesh* a_pMesh);

private:
	std::unordered_map<std::string, Mesh*> mShapes;
	static ShapeGenerator* mInstance;
};