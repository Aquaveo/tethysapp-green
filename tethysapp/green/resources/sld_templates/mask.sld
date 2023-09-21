<?xml version="1.0" encoding="ISO-8859-1"?>
<StyledLayerDescriptor version="1.0.0" xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc"
  xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.0.0/StyledLayerDescriptor.xsd">
  <NamedLayer>
    <Name>mask</Name>
    <UserStyle>
      <Name>mask</Name>
      <Title>Mask Map Style</Title>
      <Abstract>Nodata for 0 and color for 1</Abstract>
      <FeatureTypeStyle>
       <Rule>
         <RasterSymbolizer>
           <ColorMap type="values">
             <ColorMapEntry quantity="${env('inactive_val',0)}" label="Inactive" color="${env('inactive_color','#000000')}" opacity="0" />
             <ColorMapEntry quantity="${env('active_val',1)}" label="Active"   color="${env('active_color','#000000')}" />
           </ColorMap>
         </RasterSymbolizer>
       </Rule>
     </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>
